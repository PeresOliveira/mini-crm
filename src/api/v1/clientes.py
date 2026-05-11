from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from src.db.session import get_db
from src.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteOut
from src.crud import cliente as crud_cliente

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

@router.get(
    "/",
    response_model=List[ClienteOut],
    summary="Listar clientes",
    description="Retorna lista paginada de clientes com busca opcional"
)
def list_clientes(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=200, description="Máximo de registros"),
    search: Optional[str] = Query(None, description="Termo de busca (nome ou email)"),
    db: Session = Depends(get_db)
):
    """
    Lista clientes com paginação.       
    """
    clientes = crud_cliente.get_clientes(db, skip=skip, limit=limit, search=search)
    return clientes

@router.get(
    "/{cliente_id}",
    response_model=ClienteOut,
    summary="Buscar cliente por ID",
    description="Retorna os dados de um cliente específico"
)
def get_cliente(
    cliente_id: int,
    db: Session = Depends(get_db)
):
    """
    Busca cliente pelo ID.   
    """
    # Buscar cliente no banco
    db_cliente = crud_cliente.get_cliente(db, cliente_id)
    
    # Verificar se encontrou
    if not db_cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente com ID {cliente_id} não encontrado"
        )
    
    # Retornar cliente encontrado
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