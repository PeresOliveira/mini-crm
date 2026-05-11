from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal

TipoInteracao = Literal["ligacao", "email", "reuniao", "whatsapp", "proposta"]

class InteracaoBase(BaseModel):
    tipo: TipoInteracao = Field(
        ..., 
        description="Tipo de interação",
        examples=["ligacao", "email", "reuniao", "whatsapp", "proposta"]
    )
    descricao: Optional[str] = Field(
        None, 
        max_length=500,
        description="Descrição detalhada da interação"
    )

class InteracaoCreate(InteracaoBase):
    cliente_id: int = Field(..., gt=0, description="ID do cliente associado")

class InteracaoUpdate(BaseModel):
    tipo: Optional[TipoInteracao] = None
    descricao: Optional[str] = Field(None, max_length=500)

class InteracaoOut(InteracaoBase):
    id: int = Field(..., description="ID único da interação")
    cliente_id: int = Field(..., description="ID do cliente associado")
    data: datetime = Field(..., description="Data da interação")
    
    class Config:
        from_attributes = True
        
        json_schema_extra = {
            "example": {
                "id": 1,
                "cliente_id": 1,
                "tipo": "ligacao",
                "descricao": "Cliente interessado no produto",
                "data": "2024-01-01T10:00:00"
            }
        }