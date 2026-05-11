from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class ClienteBase(BaseModel):
    """
    Schema base com campos comuns a todas operações

    """
    nome: str = Field(..., min_length=1, max_length=100, description="Nome completo do cliente")
    email: EmailStr = Field(..., description="Email válido do cliente")
    telefone: Optional[str] = Field(None, max_length=20, description="Telefone para contato")

class ClienteCreate(ClienteBase):
    """
    Schema para CRIAR um cliente (POST)
    Herda todos os campos do ClienteBase
    """  
    pass

class ClienteUpdate(BaseModel):
    """
    Schema para ATUALIZAR um cliente (PUT)
    Todos campos são opcionais
    """  
    nome: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    telefone: Optional[str] = Field(None, max_length=20)

class ClienteOut(ClienteBase):
    """
    Schema para RESPOSTA da API (GET)
    Inclui campos gerados pelo sistema
    """
    id: int = Field(..., description="ID único do cliente")
    data_cadastro: datetime = Field(..., description="Data de cadastro no sistema")
    
    class Config:
        # Permite converter objetos SQLAlchemy 
        from_attributes = True 

        # Exemplo de configuração adicional
        json_schema_extra = {
            "example": {
                "id": 1,
                "nome": "João Silva",
                "email": "joao@exemplo.com",
                "telefone": "11999999999",
                "data_cadastro": "2024-01-01T10:00:00"
            }
        }