from sqlalchemy.orm import Session
from sqlalchemy import desc
from src.models.interacao import Interacao
from src.schemas.interacao import InteracaoCreate, InteracaoUpdate
from typing import Optional, List
from datetime import datetime
from src.schemas.filters import InteracaoFilters
from sqlalchemy import desc, asc

def get_interacao(db: Session, interacao_id: int):
    return db.query(Interacao).filter(Interacao.id == interacao_id).first()

def get_interacoes_por_cliente(
    db: Session, 
    cliente_id: int,
    skip: int = 0,
    limit: int = 100,
    tipo: Optional[str] = None,
    data_inicio: Optional[datetime] = None,
    data_fim: Optional[datetime] = None
):
    query = db.query(Interacao).filter(Interacao.cliente_id == cliente_id)
    
    if tipo:
        query = query.filter(Interacao.tipo == tipo)
    
    if data_inicio:
        query = query.filter(Interacao.data >= data_inicio)
    
    if data_fim:
        query = query.filter(Interacao.data <= data_fim)
    
    return query.order_by(desc(Interacao.data)).offset(skip).limit(limit).all()

def count_interacoes_por_cliente(
    db: Session,
    cliente_id: int,
    tipo: Optional[str] = None
):
    query = db.query(Interacao).filter(Interacao.cliente_id == cliente_id)
    
    if tipo:
        query = query.filter(Interacao.tipo == tipo)
    
    return query.count()

def create_interacao(db: Session, interacao: InteracaoCreate):
    interacao_data = interacao.model_dump()
    
    db_interacao = Interacao(**interacao_data)
    
    db.add(db_interacao)
    db.commit()
    db.refresh(db_interacao)
    
    return db_interacao

def update_interacao(
    db: Session,
    interacao_id: int,
    interacao_update: InteracaoUpdate
):
    db_interacao = get_interacao(db, interacao_id)
    
    if not db_interacao:
        return None
    
    update_data = interacao_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        if value is not None:
            setattr(db_interacao, field, value)
    
    db.commit()
    db.refresh(db_interacao)
    
    return db_interacao

def delete_interacao(db: Session, interacao_id: int):
    db_interacao = get_interacao(db, interacao_id)
    
    if not db_interacao:
        return False
    
    db.delete(db_interacao)
    db.commit()
    
    return True

def get_resumo_interacoes(db: Session, cliente_id: int):
    from sqlalchemy import func
    
    tipos_count = db.query(
        Interacao.tipo,
        func.count(Interacao.id).label('total')
    ).filter(
        Interacao.cliente_id == cliente_id
    ).group_by(
        Interacao.tipo
    ).all()
    
    ultima_interacao = db.query(Interacao).filter(
        Interacao.cliente_id == cliente_id
    ).order_by(
        desc(Interacao.data)
    ).first()
    
    return {
        "total": count_interacoes_por_cliente(db, cliente_id),
        "por_tipo": {tipo: total for tipo, total in tipos_count},
        "ultima_interacao": {
            "data": ultima_interacao.data,
            "tipo": ultima_interacao.tipo,
            "descricao": ultima_interacao.descricao
        } if ultima_interacao else None
    }
def get_estatisticas_cliente(db: Session, cliente_id: int):
    # Retorna estatísticas das interações de um cliente: total por tipo.
    from sqlalchemy import func
    from src.models.interacao import Interacao

    stats = (
        db.query(Interacao.tipo, func.count(Interacao.id).label("total"))
        .filter(Interacao.cliente_id == cliente_id)
        .group_by(Interacao.tipo)
        .all()
    )
    # Converte para dicionário: {"ligacao": 2, "email": 1, ...}
    return {stat[0]: stat[1] for stat in stats}

def get_interacoes_por_cliente_com_filtros(
    db: Session,
    cliente_id: int,
    skip: int = 0,
    limit: int = 100,
    filters: InteracaoFilters = None
):
    """Busca interações de um cliente com filtros e ordenação."""
    query = db.query(Interacao).filter(Interacao.cliente_id == cliente_id)
    
    if filters:
        if filters.tipo:
            query = query.filter(Interacao.tipo == filters.tipo)
        if filters.data_start:
            query = query.filter(Interacao.data >= filters.data_start)
        if filters.data_end:
            query = query.filter(Interacao.data <= filters.data_end)
        if filters.descricao_contains:
            query = query.filter(Interacao.descricao.ilike(f"%{filters.descricao_contains}%"))
        
        # Ordenação
        ordem = filters.ordem if filters.ordem else "desc"
        if filters.ordenar_por == "data":
            campo = Interacao.data
        elif filters.ordenar_por == "tipo":
            campo = Interacao.tipo
        else:
            campo = Interacao.id
        
        if ordem == "asc":
            query = query.order_by(campo.asc())
        else:
            query = query.order_by(campo.desc())
    else:
        query = query.order_by(desc(Interacao.data))
    
    return query.offset(skip).limit(limit).all()