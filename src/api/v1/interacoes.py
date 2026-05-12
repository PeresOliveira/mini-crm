from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from src.db.session import get_db
from src.schemas.interacao import (
    InteracaoCreate,
    InteracaoUpdate,
    InteracaoOut,
    TIPOS_INTERACAO
)
from src.crud import interacao as crud_interacao
from src.crud import cliente as crud_cliente

router = APIRouter(
    prefix="/interacoes",
    tags=["interacoes"],
    responses={
        404: {"description": "Recurso não encontrado"},
        422: {"description": "Dados inválidos"}
    }
)

@router.post(
    "/",
    response_model=InteracaoOut,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nova interação",
    description="Registra um novo contato/interação com um cliente"
)
def create_interacao(
    interacao: InteracaoCreate,
    db: Session = Depends(get_db)
):
    cliente = crud_cliente.get_cliente(db, interacao.cliente_id)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente com ID {interacao.cliente_id} não encontrado"
        )
    
    # Criar interação
    nova_interacao = crud_interacao.create_interacao(db, interacao)
    return nova_interacao

@router.get(
    "/cliente/{cliente_id}",
    response_model=List[InteracaoOut],
    summary="Listar interações do cliente",
    description="Retorna todas interações de um cliente específico"
)
def list_interacoes_cliente(
    cliente_id: int,
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=200, description="Máximo de registros"),
    tipo: Optional[str] = Query(None, description="Filtrar por tipo de interação"),
    db: Session = Depends(get_db)
):
    cliente = crud_cliente.get_cliente(db, cliente_id)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente com ID {cliente_id} não encontrado"
        )
    
    if tipo and tipo not in ['ligacao', 'email', 'reuniao', 'whatsapp', 'proposta']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tipo inválido. Use: ligacao, email, reuniao, whatsapp, proposta"
        )
    
    interacoes = crud_interacao.get_interacoes_por_cliente(
        db, cliente_id, skip=skip, limit=limit, tipo=tipo
    )
    return interacoes

@router.get(
    "/{interacao_id}",
    response_model=InteracaoOut,
    summary="Buscar interação por ID",
    description="Retorna detalhes de uma interação específica"
)
def get_interacao(
    interacao_id: int,
    db: Session = Depends(get_db)
):
    interacao = crud_interacao.get_interacao(db, interacao_id)
    if not interacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Interação com ID {interacao_id} não encontrada"
        )
    return interacao

@router.put(
    "/{interacao_id}",
    response_model=InteracaoOut,
    summary="Atualizar interação",
    description="Atualiza os dados de uma interação existente"
)
def update_interacao(
    interacao_id: int,
    interacao_update: InteracaoUpdate,
    db: Session = Depends(get_db)
):
    interacao = crud_interacao.get_interacao(db, interacao_id)
    if not interacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Interação com ID {interacao_id} não encontrada"
        )
    
    # Atualizar
    interacao_atualizada = crud_interacao.update_interacao(
        db, interacao_id, interacao_update
    )
    return interacao_atualizada

@router.delete(
    "/{interacao_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover interação",
    description="Remove uma interação do sistema"
)
def delete_interacao(
    interacao_id: int,
    db: Session = Depends(get_db)
):
    interacao = crud_interacao.get_interacao(db, interacao_id)
    if not interacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Interação com ID {interacao_id} não encontrada"
        )
    
    success = crud_interacao.delete_interacao(db, interacao_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao remover interação"
        )
    
    return None

@router.get(
    "/cliente/{cliente_id}/estatisticas",
    summary="Estatísticas de interações",
    description="Retorna estatísticas das interações de um cliente"
)
def get_estatisticas_interacoes(
    cliente_id: int,
    db: Session = Depends(get_db)
):
    cliente = crud_cliente.get_cliente(db, cliente_id)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente com ID {cliente_id} não encontrado"
        )
    
    # Buscar estatísticas
    stats = crud_interacao.get_estatisticas_cliente(db, cliente_id)
    total = sum(stats.values())
    
    return {
        "cliente_id": cliente_id,
        "cliente_nome": cliente.nome,
        "total_interacoes": total,
        "detalhes_por_tipo": stats
    }