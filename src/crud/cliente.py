from sqlalchemy.orm import Session
from src.models.cliente import Cliente
from src.schemas.cliente import ClienteCreate, ClienteUpdate
from src.schemas.filters import ClienteFilters

def get_cliente(db: Session, cliente_id: int):
    """
    Busca um cliente pelo ID
    """
    return db.query(Cliente).filter(Cliente.id == cliente_id).first()

def get_cliente_by_email(db: Session, email: str):
    """
    Busca um cliente pelo email
    """
    return db.query(Cliente).filter(Cliente.email == email).first()

def get_clientes(db: Session, skip: int = 0, limit: int = 100, filters: ClienteFilters = None):
    if filters is None:
        filters = ClienteFilters()
    query = db.query(Cliente)
    if filters.nome_contains:
        query = query.filter(Cliente.nome.ilike(f"%{filters.nome_contains}%"))
    if filters.email_contains:
        query = query.filter(Cliente.email.ilike(f"%{filters.email_contains}%"))
    if filters.telefone_contains:
        query = query.filter(Cliente.telefone.ilike(f"%{filters.telefone_contains}%"))
    if filters.data_cadastro_start:
        query = query.filter(Cliente.data_cadastro >= filters.data_cadastro_start)
    if filters.data_cadastro_end:
        query = query.filter(Cliente.data_cadastro <= filters.data_cadastro_end)

    campo = getattr(Cliente, filters.ordenar_por, Cliente.id)
    if filters.ordem == "asc":
        query = query.order_by(campo.asc())
    else:
        query = query.order_by(campo.desc())

    return query.offset(skip).limit(limit).all()
    

def count_clientes(db: Session, search: str = None):
    """
    Conta total de clientes 
    """
    query = db.query(Cliente)
    
    if search:
        query = query.filter(
            (Cliente.nome.contains(search)) | 
            (Cliente.email.contains(search))
        )
    
    return query.count()

def create_cliente(db: Session, cliente: ClienteCreate):
    """
    Cria um novo cliente no banco
    """
    # Converte dados para dicionário
    cliente_data = cliente.model_dump()
    
    # Remove campos None 
    cliente_data = {k: v for k, v in cliente_data.items() if v is not None}
    
    # Cria instância do modelo
    db_cliente = Cliente(**cliente_data)
    
    # Adiciona ao banco
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    
    return db_cliente

def update_cliente(
    db: Session, 
    cliente_id: int, 
    cliente_update: ClienteUpdate
):
    """
    Atualiza um cliente existente
    """
    # Busca cliente
    db_cliente = get_cliente(db, cliente_id)
    
    if not db_cliente:
        return None
    
    # Pega apenas campos que foram enviados
    update_data = cliente_update.model_dump(exclude_unset=True)
    
    # Remove None values
    update_data = {k: v for k, v in update_data.items() if v is not None}
    
    # Atualiza cada campo
    for field, value in update_data.items():
        setattr(db_cliente, field, value)
    
    # Salva no banco
    db.commit()
    db.refresh(db_cliente)
    
    return db_cliente

def delete_cliente(db: Session, cliente_id: int):
    """
    Remove um cliente do banco
    """
    db_cliente = get_cliente(db, cliente_id)
    
    if not db_cliente:
        return False
    
    db.delete(db_cliente)
    db.commit()
    
    return True

def count_clientes_filtrados(db: Session, filters: ClienteFilters = None):
    """Conta total de clientes que atendem aos filtros."""
    if filters is None:
        filters = ClienteFilters()
    
    query = db.query(Cliente)
    if filters.nome_contains:
        query = query.filter(Cliente.nome.ilike(f"%{filters.nome_contains}%"))
    if filters.email_contains:
        query = query.filter(Cliente.email.ilike(f"%{filters.email_contains}%"))
    if filters.telefone_contains:
        query = query.filter(Cliente.telefone.ilike(f"%{filters.telefone_contains}%"))
    if filters.data_cadastro_start:
        query = query.filter(Cliente.data_cadastro >= filters.data_cadastro_start)
    if filters.data_cadastro_end:
        query = query.filter(Cliente.data_cadastro <= filters.data_cadastro_end)
    
    return query.count()