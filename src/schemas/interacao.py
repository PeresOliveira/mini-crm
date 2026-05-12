from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal

TIPOS_INTERACAO = Literal['ligacao', 'email', 'reuniao', 'whatsapp', 'proposta']

class InteracaoBase(BaseModel):
    tipo: TIPOS_INTERACAO = Field(
        ..., 
        description="Tipo de interação: ligacao, email, reuniao, whatsapp, proposta"
    )
    descricao: Optional[str] = Field(
        None, 
        max_length=500,
        description="Descrição detalhada da interação"
    )

class InteracaoCreate(InteracaoBase):
    cliente_id: int = Field(..., gt=0, description="ID do cliente associado")

class InteracaoUpdate(BaseModel):
    tipo: Optional[TIPOS_INTERACAO] = None
    descricao: Optional[str] = Field(None, max_length=500)

class InteracaoOut(InteracaoBase):
    id: int = Field(..., description="ID único da interação")
    cliente_id: int = Field(..., description="ID do cliente associado")
    data: datetime = Field(..., description="Data da interação")
    
    class ConfigDict:
        from_attributes = True
        
        json_schema_extra = {
            "example": {
                "id": 1,
                "cliente_id": 1,
                "tipo": "ligacao",
                "descricao": "Cliente interessado no produto X",
                "data": "2024-01-01T10:00:00"
            }
        }