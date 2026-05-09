from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from src.db.base import Base

class Cliente(Base):
    """
    Modelo de Cliente - Representa a tabela 'clientes' no banco de dados
    
    Campos:
    - id: Identificador único (auto-incremento)
    - nome: Nome completo do cliente
    - email: Email único para contato
    - telefone: Número de telefone (opcional)
    - data_cadastro: Data de quando o cliente foi cadastrado
    """
    
    __tablename__ = "clientes"  
    
    # Colunas da tabela
    id = Column(Integer, primary_key=True, index=True)
    """ID auto-incrementável, chave primária"""
    
    nome = Column(String(100), nullable=False)
    """Nome do cliente - não pode ser vazio"""
    
    email = Column(String(100), unique=True, index=True, nullable=False)
    """Email - único no sistema, não pode repetir"""
    
    telefone = Column(String(20), nullable=True)
    """Telefone - opcional (pode ser vazio)"""
    
    data_cadastro = Column(DateTime(timezone=True), server_default=func.now())
    """Data do cadastro - preenchida automaticamente"""
    
    def __repr__(self):
        """Representação textual do objeto (útil para debug)"""
        return f"<Cliente(id={self.id}, nome='{self.nome}', email='{self.email}')>"