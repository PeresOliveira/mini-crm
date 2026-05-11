"""
Script para popular banco com dados realistas de clientes e interações
Executar: python scripts/populate_full_data.py
"""
import sys
from pathlib import Path
import random
from datetime import datetime, timedelta
sys.path.append(str(Path(__file__).parent.parent))

from src.db.session import SessionLocal
from src.crud import cliente as crud_cliente
from src.crud import interacao as crud_interacao
from src.schemas.cliente import ClienteCreate
from src.schemas.interacao import InteracaoCreate

# Dados para geração
NOMES = [
    "João Silva", "Maria Santos", "Pedro Oliveira", "Ana Costa", 
    "Lucas Lima", "Fernanda Souza", "Rafaela Rodrigues", "Carlos Ferreira",
    "Juliana Almeida", "Ricardo Pereira", "Patrícia Gomes", "Eduardo Martins"
]

EMAILS = [
    "@gmail.com", "@hotmail.com", "@outlook.com", "@empresa.com.br"
]

TIPOS_INTERACAO = ["ligacao", "email", "reuniao", "whatsapp", "proposta"]
DESCRICOES = [
    "Primeiro contato - cliente interessado",
    "Enviada proposta comercial",
    "Reunião de apresentação",
    "Follow-up após reunião",
    "Negociação de valores",
    "Fechamento de contrato",
    "Pós-venda",
    "Solicitação de orçamento"
]

def gerar_clientes(db, quantidade=15):
    """Gera clientes aleatórios"""
    clientes_ids = []
    
    for i, nome in enumerate(NOMES[:quantidade]):
        # Gerar email a partir do nome
        nome_partes = nome.lower().split()
        email_base = f"{nome_partes[0]}.{nome_partes[1] if len(nome_partes) > 1 else 'silva'}"
        email = f"{email_base}{random.choice(EMAILS)}"
        
        # Telefone aleatório
        telefone = f"119{random.randint(10000000, 99999999)}"
        
        cliente_data = ClienteCreate(
            nome=nome,
            email=email,
            telefone=telefone
        )
        
        try:
            cliente = crud_cliente.create_cliente(db, cliente_data)
            clientes_ids.append(cliente.id)
            print(f"Cliente {cliente.id}: {cliente.nome}")
        except Exception as e:
            print(f"Erro ao criar {nome}: {e}")
    
    return clientes_ids

def gerar_interacoes(db, clientes_ids, max_por_cliente=10):
    """Gera interações aleatórias para cada cliente"""
    total = 0
    
    for cliente_id in clientes_ids:
        # Número aleatório de interações (1 a max_por_cliente)
        num_interacoes = random.randint(1, max_por_cliente)
        
        for _ in range(num_interacoes):
            # Data aleatória nos últimos 90 dias
            dias_atras = random.randint(0, 90)
            data_interacao = datetime.now() - timedelta(days=dias_atras)
            
            interacao_data = InteracaoCreate(
                cliente_id=cliente_id,
                tipo=random.choice(TIPOS_INTERACAO),
                descricao=random.choice(DESCRICOES)
            )
            
            try:
                # Inserir diretamente no banco (para usar data específica)
                from src.models.interacao import Interacao
                interacao = Interacao(
                    cliente_id=interacao_data.cliente_id,
                    tipo=interacao_data.tipo,
                    descricao=interacao_data.descricao,
                    data=data_interacao
                )
                db.add(interacao)
                db.commit()
                total += 1
            except Exception as e:
                print(f"Erro ao criar interação: {e}")
                db.rollback()
        
        print(f"Cliente {cliente_id}: {num_interacoes} interações")
    
    return total

def main():
    print("Iniciando população do banco com dados realistas...")
    
    db = SessionLocal()
    
    try:
        # Limpar dados existentes 
        resposta = input("Deseja limpar dados existentes? (s/N): ")
        if resposta.lower() == 's':
            from src.models.interacao import Interacao
            from src.models.cliente import Cliente
            
            db.query(Interacao).delete()
            db.query(Cliente).delete()
            db.commit()
            print("Dados antigos removidos")
        
        # Gerar clientes
        print("\nCriando clientes...")
        clientes_ids = gerar_clientes(db, quantidade=12)
        
        # Gerar interações
        print("\nCriando interações...")
        total_interacoes = gerar_interacoes(db, clientes_ids, max_por_cliente=8)
        
        # Estatísticas
        print("\nRESUMO FINAL:")
        print(f"Clientes criados: {len(clientes_ids)}")
        print(f"Interações criadas: {total_interacoes}")
        print(f"Média por cliente: {total_interacoes/len(clientes_ids):.1f}")
        
    finally:
        db.close()

if __name__ == "__main__":
    main()