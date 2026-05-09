from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.models import Cliente

app = FastAPI(
    title="Mini CRM API",
    description="Sistema de gestão de clientes e interações",
    version="0.1.0"
)

@app.get("/")
def root():
    
    return {
        "message": "Mini CRM API is running",
        "status": "online",
        "version": "0.1.0"
    }

@app.get("/health")
def health_check():
   
    return {
        "status": "healthy",
        "service": "mini-crm-api",
        "timestamp": "2024-01-01"
    }
@app.get("/test-db")
def test_database_connection(db: Session = Depends(get_db)):
    try:
        total_clientes = db.query(Cliente).count()
        return {
            "status": "connected",
            "database": "SQLite",
            "total_clientes": total_clientes,
            "message": "Banco de dados funcionando!"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
    
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schema para criar cliente
class ClienteCreate(BaseModel):
    nome: str
    email: str
    telefone: Optional[str] = None

@app.post("/clientes/test")
def criar_cliente_teste(cliente: ClienteCreate, db: Session = Depends(get_db)):
    """
    Endpoint temporário para testar inserção no banco
    """
    try:
        # Criar novo cliente
        novo_cliente = Cliente(
            nome=cliente.nome,
            email=cliente.email,
            telefone=cliente.telefone
        )
        
        # Adicionar ao banco
        db.add(novo_cliente)
        db.commit()
        db.refresh(novo_cliente)  # Atualiza com o ID gerado
        
        return {
            "message": "Cliente criado com sucesso!",
            "cliente": {
                "id": novo_cliente.id,
                "nome": novo_cliente.nome,
                "email": novo_cliente.email,
                "telefone": novo_cliente.telefone,
                "data_cadastro": novo_cliente.data_cadastro
            }
        }
    except Exception as e:
        return {
            "error": str(e)
        }