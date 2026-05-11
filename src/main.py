from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1 import clientes

# Criar aplicação
app = FastAPI(
    title="Mini CRM API",
    description="Sistema de Gestão de Clientes",
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
    allow_origins=["*"],  # Em produção, especifique origens
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(clientes.router)

# Endpoints de teste
@app.get("/")
def root():
    return {
        "message": "Mini CRM API is running",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "mini-crm-api"
    }

@app.get("/info")
def info():    
    return {
        "name": "Mini CRM",
        "version": "1.0.0",
        "endpoints": {
            "clientes": "/clientes",
            "docs": "/docs"
        }
    }