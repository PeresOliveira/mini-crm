from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from src.db.session import get_db
from src.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteOut
from src.crud import cliente as crud_cliente
from src.schemas.filters import ClienteFilters
from datetime import datetime

router = APIRouter(
    prefix="/clientes",
    tags=["clientes"],
    responses={
        404: {"description": "Cliente não encontrado"},
        422: {"description": "Dados inválidos"}
    }
)

@router.post(
    "/",
    response_model=ClienteOut,
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo cliente",
    description="Cria um cliente com os dados fornecidos. Email deve ser único."
)
def create_cliente(
    cliente: ClienteCreate,
    db: Session = Depends(get_db)
):
    """
    Endpoint para criar um novo cliente.
    """
    #Verificar se o email já existe
    existing_cliente = crud_cliente.get_cliente_by_email(db, cliente.email)
    if existing_cliente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email '{cliente.email}' já está cadastrado."
        )
    return crud_cliente.create_cliente(db, cliente)

@router.get("/", response_model=List[ClienteOut])
def list_clientes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    nome_contains: Optional[str] = Query(None),
    email_contains: Optional[str] = Query(None),
    telefone_contains: Optional[str] = Query(None),
    data_cadastro_start: Optional[datetime] = Query(None),
    data_cadastro_end: Optional[datetime] = Query(None),
    ordenar_por: str = Query("id", pattern="^(id|nome|email|data_cadastro)$"),
    ordem: str = Query("desc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    filters = ClienteFilters(
        nome_contains=nome_contains,
        email_contains=email_contains,
        telefone_contains=telefone_contains,
        data_cadastro_start=data_cadastro_start,
        data_cadastro_end=data_cadastro_end,
        ordenar_por=ordenar_por,
        ordem=ordem
    )
    clientes = crud_cliente.get_clientes(db, skip=skip, limit=limit, filters=filters)
    return clientes

@router.get("/count", summary="Contar clientes com filtros")
def count_clientes(
    nome_contains: Optional[str] = Query(None),
    email_contains: Optional[str] = Query(None),
    telefone_contains: Optional[str] = Query(None),
    data_cadastro_start: Optional[datetime] = Query(None),
    data_cadastro_end: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    from src.schemas.filters import ClienteFilters
    filters = ClienteFilters(
        nome_contains=nome_contains,
        email_contains=email_contains,
        telefone_contains=telefone_contains,
        data_cadastro_start=data_cadastro_start,
        data_cadastro_end=data_cadastro_end
    )
    total = crud_cliente.count_clientes_filtrados(db, filters)
    return {"total": total}

@router.get(
    "/{cliente_id}",
    response_model=ClienteOut,
    summary="Buscar cliente por ID",
    description="Retorna os dados de um cliente específico"
)
def get_cliente(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = crud_cliente.get_cliente(db, cliente_id)
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return db_cliente

@router.put(
    "/{cliente_id}",
    response_model=ClienteOut,
    summary="Atualizar cliente",
    description="Atualiza parcialmente um cliente existente"
)
def update_cliente(
    cliente_id: int,
    cliente_update: ClienteUpdate,
    db: Session = Depends(get_db)
):
    """
    Atualiza dados de um cliente.
    """
     # Verificar se cliente existe
    db_cliente = crud_cliente.get_cliente(db, cliente_id)
    if not db_cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente com ID {cliente_id} não encontrado"
        )
    
    # Se estiver atualizando email, verificar se novo email não pertence a outro cliente
    if cliente_update.email and cliente_update.email != db_cliente.email:
        existing = crud_cliente.get_cliente_by_email(db, cliente_update.email)
        if existing and existing.id != cliente_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email '{cliente_update.email}' já está em uso"
            )
    # Atualizar cliente
    updated_cliente = crud_cliente.update_cliente(db, cliente_id, cliente_update)
    return updated_cliente

@router.delete(
    "/{cliente_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover cliente",
    description="Remove um cliente do sistema"
)
def delete_cliente(
    cliente_id: int,
    db: Session = Depends(get_db)
):
    """
    Remove um cliente.
    """
     # Verificar se cliente existe
    db_cliente = crud_cliente.get_cliente(db, cliente_id)
    if not db_cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente com ID {cliente_id} não encontrado"
        )
    
    # Remover cliente
    success = crud_cliente.delete_cliente(db, cliente_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao remover cliente"
        )
    
    # 204 NO CONTENT não retorna corpo
    return None