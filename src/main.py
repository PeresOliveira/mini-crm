from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1 import clientes, interacoes, analytics
from src.api.v1 import clientes, interacoes  

app = FastAPI(
    title="Mini CRM API",
    description="""
    ## Sistema de Gestão de Clientes
    
    API para gerenciar clientes e interações comerciais.
    
    ### Funcionalidades:
    * CRUD completo de clientes
    * Busca e paginação
    * Gerenciamento de interações
    * Histórico de contato
    * Estatísticas de interações
    
    ### Documentação:
    * Swagger UI: `/docs`
    * ReDoc: `/redoc`
    """,
    version="1.0.0",
    contact={
        "name": "Seu Nome",
        "email": "seuemail@exemplo.com",
    },
    license_info={
        "name": "MIT",
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clientes.router)
app.include_router(interacoes.router)
app.include_router(analytics.router)

@app.get("/")
def root():
    return {
        "message": "Mini CRM API is running",
        "version": "1.0.0",
        "endpoints": {
            "clientes": "/clientes",
            "interacoes": "/interacoes",
            "docs": "/docs"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/info")
def info():
    return {
        "name": "Mini CRM",
        "version": "1.0.0",
        "endpoints_count": {
            "clientes": 5,
            "interacoes": 6
        }
    }
