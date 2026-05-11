from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List
from src.schemas.interacao import InteracaoOut  

class ClienteBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=100)
    email: EmailStr = Field(...)
    telefone: Optional[str] = Field(None, max_length=20)

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    telefone: Optional[str] = Field(None, max_length=20)

class ClienteOut(ClienteBase):
    id: int
    data_cadastro: datetime
    interacoes: List[InteracaoOut] = []  
    class Config:
        from_attributes = True
        
        json_schema_extra = {
            "example": {
                "id": 1,
                "nome": "João Silva",
                "email": "joao@exemplo.com",
                "telefone": "11999999999",
                "data_cadastro": "2024-01-01T10:00:00",
                "interacoes": [
                    {
                        "id": 1,
                        "cliente_id": 1,
                        "tipo": "ligacao",
                        "descricao": "Primeiro contato",
                        "data": "2024-01-01T10:00:00"
                    }
                ]
            }
        }