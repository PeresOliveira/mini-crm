from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from src.db.session import get_db
from src.schemas.interacao import (
    InteracaoCreate, 
    InteracaoUpdate, 
    InteracaoOut
)
from src.crud import interacao as crud_interacao
from src.crud import cliente as crud_cliente

router = APIRouter(
    prefix="/interacoes",
    tags=["interacoes"],
    responses={
        404: {"description": "Interação ou cliente não encontrado"},
        422: {"description": "Dados inválidos"}
    }
)

@router.post(
    "/",
    response_model=InteracaoOut,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nova interação",
    description="Registra uma interação com um cliente existente"
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
    
    return crud_interacao.create_interacao(db, interacao)

@router.get(
    "/cliente/{cliente_id}",
    response_model=List[InteracaoOut],
    summary="Listar interações de um cliente",
    description="Retorna todas as interações de um cliente específico"
)
def list_interacoes_cliente(
    cliente_id: int,
    skip: int = Query(0, ge=0, description="Pular N registros"),
    limit: int = Query(100, ge=1, le=200, description="Limite de registros"),
    tipo: Optional[str] = Query(None, description="Filtrar por tipo"),
    data_inicio: Optional[datetime] = Query(None, description="Data inicial (YYYY-MM-DD)"),
    data_fim: Optional[datetime] = Query(None, description="Data final (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    cliente = crud_cliente.get_cliente(db, cliente_id)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente com ID {cliente_id} não encontrado"
        )
    
    interacoes = crud_interacao.get_interacoes_por_cliente(
        db, 
        cliente_id=cliente_id,
        skip=skip,
        limit=limit,
        tipo=tipo,
        data_inicio=data_inicio,
        data_fim=data_fim
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
    
    updated = crud_interacao.update_interacao(db, interacao_id, interacao_update)
    return updated

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
    "/cliente/{cliente_id}/resumo",
    summary="Resumo de interações",
    description="Estatísticas das interações de um cliente"
)
def get_resumo_interacoes(
    cliente_id: int,
    db: Session = Depends(get_db)
):
    cliente = crud_cliente.get_cliente(db, cliente_id)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente com ID {cliente_id} não encontrado"
        )
    
    resumo = crud_interacao.get_resumo_interacoes(db, cliente_id)
    return resumo