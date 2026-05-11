from sqlalchemy.orm import Session
from src.models.cliente import Cliente
from src.schemas.cliente import ClienteCreate, ClienteUpdate

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

def get_clientes(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    search: str = None
):
    """
    Lista clientes com paginação e busca opcional
    """
    
    query = db.query(Cliente)  

    # Se tiver termo de busca, filtra por nome ou email
    if search:
        query = query.filter(
            (Cliente.nome.contains(search)) | 
            (Cliente.email.contains(search))
        )
    
    # Aplica paginação e ordena
    return query.order_by(Cliente.id.desc()).offset(skip).limit(limit).all()
    

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