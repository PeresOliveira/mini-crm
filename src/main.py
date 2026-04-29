from fastapi import FastAPI

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
        "service": "mini-crm-api"
    }