
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.main import app
from src.db.base import Base
from src.db.session import get_db
from src.models import Cliente, Interacao 

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # Necessário para SQLite em memória com múltiplas threads
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Sobrescrever a dependência get_db para usar o banco de teste
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Fixture para criar as tabelas antes de cada teste e dropar depois
@pytest.fixture(scope="function")
def db_session():
    # Criar todas as tabelas
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

# Fixture para cliente HTTP (TestClient) que será usado nos testes de API
@pytest.fixture(scope="function")
def client(db_session):
    # db_session é executado antes, garantindo banco limpo
    with TestClient(app) as test_client:
        yield test_client

# Fixture com dados de exemplo para cliente
@pytest.fixture
def sample_cliente_data():
    return {
        "nome": "Cliente Teste",
        "email": "teste@exemplo.com",
        "telefone": "11999999999"
    }

# Fixture com dados de exemplo para interação
@pytest.fixture
def sample_interacao_data():
    return {
        "tipo": "ligacao",
        "descricao": "Teste de interação"
    }