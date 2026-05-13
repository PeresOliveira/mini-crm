import pytest
from unittest.mock import patch, MagicMock
from scripts.seed_db import seed_database, limpar_banco
from scripts.seed_db import limpar_banco
from src.schemas.cliente import ClienteCreate
from src.schemas.interacao import InteracaoCreate
from unittest.mock import MagicMock, call
from src.models import Cliente, Interacao

# Fixture para simular uma sessão de banco
@pytest.fixture
def mock_db_session():
    with patch("scripts.seed_db.SessionLocal") as mock:
        session = MagicMock()
        mock.return_value = session
        yield session

# Teste da função limpar_banco
def test_limpar_banco(mock_db_session):
    limpar_banco(mock_db_session)
    
    # Verifica se query foi chamada para Interacao e Cliente
    mock_db_session.query.assert_any_call(Interacao)
    mock_db_session.query.assert_any_call(Cliente)
    
    # Verifica se delete e commit foram chamados
    mock_db_session.query().delete.assert_called()
    mock_db_session.commit.assert_called()
# Teste do seed sem dados existentes
@patch("scripts.seed_db.gerar_clientes_simulados")
@patch("scripts.seed_db.gerar_interacoes_simuladas")
@patch("scripts.seed_db.crud_cliente.create_cliente")
@patch("scripts.seed_db.crud_interacao.create_interacao")
def test_seed_sem_dados_existentes(
    mock_create_interacao,
    mock_create_cliente,
    mock_gerar_interacoes,
    mock_gerar_clientes,
    mock_db_session
):
    # Simular que não há clientes no banco
    mock_db_session.query().count.return_value = 0
    
    # Simular dados gerados
    mock_gerar_clientes.return_value = [
        {"nome": "Teste", "email": "teste@email.com", "telefone": "123", "data_cadastro": None}
    ]
    # Quando create_cliente for chamado, retornar objeto com id
    mock_cliente = MagicMock()
    mock_cliente.id = 1
    mock_create_cliente.return_value = mock_cliente
    
    mock_gerar_interacoes.return_value = [
        {"cliente_id": 1, "tipo": "ligacao", "descricao": "teste", "data": None}
    ]
    
    # Executar seed (limpar=False, num_clientes=1, num_interacoes=1)
    with patch("builtins.input", return_value="n"):  # evitar prompt
        seed_database(limpar=False, num_clientes=1, num_interacoes=1)
    
    # Verificar se create_cliente foi chamado com os dados corretos
    mock_create_cliente.assert_called_once()
    args, _ = mock_create_cliente.call_args
    assert isinstance(args[1], ClienteCreate)
    assert args[1].nome == "Teste"
    
    # Verificar se create_interacao foi chamado
    mock_create_interacao.assert_called_once()
    args, _ = mock_create_interacao.call_args
    assert isinstance(args[1], InteracaoCreate)
    assert args[1].cliente_id == 1

# Teste do seed com dados existentes e usuário opta por limpar
@patch("scripts.seed_db.limpar_banco")
@patch("scripts.seed_db.gerar_clientes_simulados")
@patch("scripts.seed_db.gerar_interacoes_simuladas")
@patch("scripts.seed_db.crud_cliente.create_cliente")
def test_seed_com_dados_existentes_e_limpar(
    mock_create_cliente,
    mock_gerar_interacoes,
    mock_gerar_clientes,
    mock_limpar_banco,
    mock_db_session
):
    # Simular que já existem clientes
    mock_db_session.query().count.return_value = 5
    
    # Simular resposta do usuário "s" para limpar
    with patch("builtins.input", return_value="s"):
        seed_database(limpar=False, num_clientes=2, num_interacoes=3)
    
    # Verificar que limpar_banco foi chamado
    mock_limpar_banco.assert_called_once_with(mock_db_session)
    
    # Verificar que gerou novos dados
    mock_gerar_clientes.assert_called_once_with(2)
    mock_gerar_interacoes.assert_called_once()

# Teste do seed com dados existentes e usuário opta por NÃO limpar
def test_seed_com_dados_existentes_sem_limpar(mock_db_session):
    mock_db_session.query().count.return_value = 5
    with patch("builtins.input", return_value="n"):
        seed_database(limpar=False)
    # Não deve chamar limpar_banco nem gerar novos dados
    # Mas como a função retorna cedo, não há chamadas adicionais
    # Pode-se verificar que não houve chamada para create_cliente