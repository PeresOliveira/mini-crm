import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.db.session import engine
from src.db.base import Base
from src.models import cliente 
def init_database():

    print("Iniciando criação do banco de dados...")
    print(f"Banco de dados: {engine.url}")
    
    try:
        Base.metadata.create_all(bind=engine)
        print("Tabelas criadas com sucesso!")
        
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"Tabelas criadas: {', '.join(tables)}")
        
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_database()