from src.crud import cliente as crud_cliente
from src.schemas.cliente import ClienteCreate, ClienteUpdate

def test_crud_cliente_operations(db_session):
    """Teste integrado das operações CRUD de cliente"""
    # Create
    cliente_data = ClienteCreate(
        nome="CRUD Teste",
        email="crud@teste.com",
        telefone="11999999999"
    )
    cliente = crud_cliente.create_cliente(db_session, cliente_data)
    assert cliente.id is not None
    assert cliente.nome == "CRUD Teste"
    
    # Read
    fetched = crud_cliente.get_cliente(db_session, cliente.id)
    assert fetched is not None
    assert fetched.email == "crud@teste.com"
    
    # Update
    update_data = ClienteUpdate(telefone="11888888888")
    updated = crud_cliente.update_cliente(db_session, cliente.id, update_data)
    assert updated.telefone == "11888888888"
    
    # Delete
    result = crud_cliente.delete_cliente(db_session, cliente.id)
    assert result is True
    deleted = crud_cliente.get_cliente(db_session, cliente.id)
    assert deleted is None