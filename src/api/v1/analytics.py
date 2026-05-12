from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from datetime import datetime, timedelta
from typing import Dict, Any

from src.db.session import get_db
from src.models import Cliente, Interacao

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/dashboard")
def get_dashboard_stats(db: Session = Depends(get_db)):
    total_clientes = db.query(Cliente).count()
    
    total_interacoes = db.query(Interacao).count()
    
    media_interacoes = total_interacoes / total_clientes if total_clientes > 0 else 0
    
    interacoes_por_tipo = db.query(
        Interacao.tipo, func.count(Interacao.id).label("total")
    ).group_by(Interacao.tipo).all()
    interacoes_por_tipo_dict = {tipo: total for tipo, total in interacoes_por_tipo}
    
    top_clientes = (
        db.query(
            Cliente.id, Cliente.nome, Cliente.email,
            func.count(Interacao.id).label("total_interacoes")
        )
        .join(Interacao, Cliente.id == Interacao.cliente_id)
        .group_by(Cliente.id)
        .order_by(func.count(Interacao.id).desc())
        .limit(5)
        .all()
    )
    top_clientes_list = [
        {"id": c.id, "nome": c.nome, "email": c.email, "total_interacoes": c.total_interacoes}
        for c in top_clientes
    ]
    
    data_limite = datetime.now() - timedelta(days=30)
    interacoes_ultimos_30 = db.query(Interacao).filter(Interacao.data >= data_limite).count()
    
    dias = []
    for i in range(7):
        dia = datetime.now().date() - timedelta(days=i)
        dia_inicio = datetime.combine(dia, datetime.min.time())
        dia_fim = datetime.combine(dia, datetime.max.time())
        count = db.query(Interacao).filter(
            Interacao.data >= dia_inicio,
            Interacao.data <= dia_fim
        ).count()
        dias.append({"data": dia.isoformat(), "total": count})
    
    clientes_sem_interacao = db.query(Cliente).filter(
        ~Cliente.interacoes.any()
    ).count()
    
    return {
        "total_clientes": total_clientes,
        "total_interacoes": total_interacoes,
        "media_interacoes_por_cliente": round(media_interacoes, 2),
        "interacoes_por_tipo": interacoes_por_tipo_dict,
        "top_clientes_mais_interacoes": top_clientes_list,
        "interacoes_ultimos_30_dias": interacoes_ultimos_30,
        "interacoes_por_dia_ultimos_7": dias,
        "clientes_sem_interacao": clientes_sem_interacao
    }

@router.get("/interacoes-por-mes")
def get_interacoes_por_mes(db: Session = Depends(get_db)):
    from sqlalchemy import extract
    
    resultados = db.query(
        extract('year', Interacao.data).label('ano'),
        extract('month', Interacao.data).label('mes'),
        func.count(Interacao.id).label('total')
    ).group_by('ano', 'mes').order_by('ano', 'mes').all()
    
    return [
        {"ano": int(r.ano), "mes": int(r.mes), "total": r.total}
        for r in resultados
    ]

@router.get("/conversao")
def get_conversao_estimada(db: Session = Depends(get_db)):
    """
    Métrica simples: proporção de interações que resultaram em 'proposta' 
    em relação ao total de interações.
    """
    total = db.query(Interacao).count()
    if total == 0:
        return {"total_interacoes": 0, "propostas": 0, "taxa_conversao": 0.0}
    
    propostas = db.query(Interacao).filter(Interacao.tipo == "proposta").count()
    taxa = (propostas / total) * 100
    
    return {
        "total_interacoes": total,
        "propostas": propostas,
        "taxa_conversao_percentual": round(taxa, 2)
    }