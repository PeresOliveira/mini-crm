from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ClienteFilters(BaseModel):
    nome_contains: Optional[str] = Field(None, description="Busca por parte do nome")
    email_contains: Optional[str] = Field(None, description="Busca por parte do email")
    telefone_contains: Optional[str] = Field(None, description="Busca por parte do telefone")
    data_cadastro_start: Optional[datetime] = Field(None, description="Data inicial do cadastro")
    data_cadastro_end: Optional[datetime] = Field(None, description="Data final do cadastro")
    ordenar_por: Optional[str] = Field("id", description="Campo para ordenar (id, nome, email, data_cadastro)")
    ordem: Optional[str] = Field("desc", description="asc ou desc")

class InteracaoFilters(BaseModel):
    tipo: Optional[str] = Field(None, description="Tipo da interação")
    data_start: Optional[datetime] = Field(None, description="Data inicial")
    data_end: Optional[datetime] = Field(None, description="Data final")
    descricao_contains: Optional[str] = Field(None, description="Busca por texto na descrição")
    ordenar_por: Optional[str] = Field("data", description="data, tipo, id")
    ordem: Optional[str] = Field("desc", description="asc ou desc")