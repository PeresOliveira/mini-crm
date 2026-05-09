from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    
    
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "sqlite:///./crm.db"  
    )
    
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()