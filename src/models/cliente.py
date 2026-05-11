from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.db.base import Base

class Cliente(Base):
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    telefone = Column(String(20), nullable=True)
    data_cadastro = Column(DateTime(timezone=True), server_default=func.now())

    interacoes = relationship(
        "Interacao", 
        back_populates="cliente",
        cascade="all, delete-orphan"  # Se deletar cliente, deleta interações
    )
    def __repr__(self):
        return f"<Cliente(id={self.id}, nome='{self.nome}', email='{self.email}')>"