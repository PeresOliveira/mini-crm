import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.db.session import SessionLocal
from src.models import Cliente, Interacao
from src.schemas.cliente import ClienteCreate
from src.schemas.interacao import InteracaoCreate
from src.crud import cliente as crud_cliente
from src.crud import interacao as crud_interacao
from src.utils.generate_simulated_data import (
    gerar_clientes_simulados,
    gerar_interacoes_simuladas
)

def limpar_banco(db):
    print("  Removendo dados existentes...")
    db.query(Interacao).delete()
    db.query(Cliente).delete()
    db.commit()
    print(" Dados antigos removidos com sucesso.")

def seed_database(limpar: bool = False, num_clientes: int = 50, num_interacoes: int = 150):
    db = SessionLocal()
    try:
        if limpar:
            limpar_banco(db)
        
        total_clientes_existentes = db.query(Cliente).count()
        if total_clientes_existentes > 0 and not limpar:
            resposta = input(f"  Banco já possui {total_clientes_existentes} clientes. Deseja limpar e recriar? (s/N): ")
            if resposta.lower() != 's':
                print(" Operação cancelada pelo usuário.")
                return
            limpar_banco(db)
        
        print(f"\n Gerando {num_clientes} clientes simulados...")
        clientes_data = gerar_clientes_simulados(num_clientes)
        
        clientes_ids = []
        for cliente_dict in clientes_data:
            cliente_create = ClienteCreate(**cliente_dict)
            novo_cliente = crud_cliente.create_cliente(db, cliente_create)
            clientes_ids.append(novo_cliente.id)
            print(f"   Criado: {novo_cliente.nome} (ID {novo_cliente.id})")
        
        print(f"\n {len(clientes_ids)} clientes inseridos.")
        
        print(f"\n Gerando {num_interacoes} interações simuladas...")
        interacoes_data = gerar_interacoes_simuladas(clientes_ids, num_interacoes)
        
        for i, interacao_dict in enumerate(interacoes_data, 1):
            interacao_create = InteracaoCreate(**interacao_dict)
            nova_interacao = crud_interacao.create_interacao(db, interacao_create)
            if i % 50 == 0:
                print(f"  ... {i} interações inseridas")
        
        print(f"\n {len(interacoes_data)} interações inseridas.")
        
        total_clientes = db.query(Cliente).count()
        total_interacoes = db.query(Interacao).count()
        print("\n" + "="*50)
        print(" RESUMO FINAL")
        print(f"   Clientes: {total_clientes}")
        print(f"   Interações: {total_interacoes}")
        
        from sqlalchemy import func
        stats = db.query(
            Interacao.tipo, func.count(Interacao.id)
        ).group_by(Interacao.tipo).all()
        print("\n Interações por tipo:")
        for tipo, count in stats:
            print(f"   {tipo}: {count}")
        print("="*50)
        
    except Exception as e:
        print(f"\n ERRO durante o seed: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Popula o banco com dados simulados.")
    parser.add_argument("--clear", action="store_true", help="Remove dados existentes antes de inserir")
    parser.add_argument("--clientes", type=int, default=50, help="Número de clientes a gerar")
    parser.add_argument("--interacoes", type=int, default=150, help="Número de interações a gerar")
    args = parser.parse_args()
    
    seed_database(
        limpar=args.clear,
        num_clientes=args.clientes,
        num_interacoes=args.interacoes
    )