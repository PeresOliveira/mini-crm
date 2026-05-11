from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.db.base import Base

class Interacao(Base):
    __tablename__ = "interacoes"
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(
        Integer, 
        ForeignKey("clientes.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    tipo = Column(String(50), nullable=False)
    descricao = Column(Text, nullable=True)
    data = Column(DateTime(timezone=True), server_default=func.now())
    cliente = relationship("Cliente", back_populates="interacoes")
    def __repr__(self):
        return f"<Interacao(id={self.id}, cliente_id={self.cliente_id}, tipo='{self.tipo}')>"
    