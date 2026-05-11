import random
from datetime import datetime, timedelta
from typing import List, Dict, Any
NOMES_MASC = [
    "João", "Pedro", "Lucas", "Rafael", "Carlos", "Roberto", "Thiago", 
    "Bruno", "Felipe", "Diego", "André", "Ricardo", "Marcelo", "Alexandre"
]
NOMES_FEM = [
    "Ana", "Maria", "Juliana", "Fernanda", "Patrícia", "Camila", "Larissa",
    "Letícia", "Amanda", "Vanessa", "Carolina", "Beatriz", "Bruna", "Cristina"
]
SOBRENOMES = [
    "Silva", "Santos", "Oliveira", "Costa", "Lima", "Souza", "Pereira",
    "Alves", "Rodrigues", "Gomes", "Nogueira", "Rocha", "Mendes", "Carvalho"
]

DOMINIOS_EMAIL = [
    "gmail.com", "hotmail.com", "outlook.com", "yahoo.com.br",
    "empresa.com.br", "consultoria.com", "techmail.com", "provedor.com"
]

TIPOS_INTERACAO = ["ligacao", "email", "reuniao", "whatsapp", "proposta"]

DESCRICOES_POR_TIPO = {
    "ligacao": [
        "Primeiro contato telefônico – cliente demonstrou interesse.",
        "Retorno de ligação – cliente não atendeu, deixado recado.",
        "Ligação de follow-up – cliente pediu para ligar depois.",
        "Conversa sobre necessidades específicas – duração média.",
        "Agendamento de reunião presencial via telefone.",
        "Cliente solicitou orçamento – enviei por email após a ligação."
    ],
    "email": [
        "Envio de catálogo de produtos e tabela de preços.",
        "Resposta a dúvida sobre prazos de entrega.",
        "Envio de proposta comercial (PDF anexo).",
        "Solicitação de documentos para cadastro.",
        "Confirmação de recebimento de pagamento.",
        "Newsletter mensal – cliente abriu o email."
    ],
    "reuniao": [
        "Reunião inicial de alinhamento de expectativas.",
        "Demonstração ao vivo do sistema (online).",
        "Negociação de contrato – ajustes nos termos.",
        "Alinhamento técnico com equipe do cliente.",
        "Fechamento de parceria – assinatura de contrato.",
        "Reunião pós-venda para avaliar satisfação."
    ],
    "whatsapp": [
        "Envio de link para reunião virtual.",
        "Cliente enviou áudio com dúvida rápida.",
        "Compartilhamento de material de apoio (PDF).",
        "Lembrete de horário da reunião agendada.",
        "Cliente confirmou presença via WhatsApp.",
        "Envio de vídeo explicativo sobre funcionalidade."
    ],
    "proposta": [
        "Proposta comercial padrão enviada por email.",
        "Revisão da proposta solicitada – alteração de escopo.",
        "Proposta personalizada com descontos.",
        "Aceite parcial da proposta – aguardando assinatura.",
        "Contraproposta recebida – análise em andamento.",
        "Proposta aprovada – cliente efetuou o pagamento."
    ]
}

def _nome_aleatorio() -> str:
    genero = random.choice(["M", "F"])
    primeiro = random.choice(NOMES_MASC if genero == "M" else NOMES_FEM)
    sobrenome = random.choice(SOBRENOMES)
    return f"{primeiro} {sobrenome}"

def _email_aleatorio(nome: str) -> str:
    base = nome.lower().replace(" ", ".")
    base = ''.join(c for c in base if c.isalnum() or c == '.')
    dominio = random.choice(DOMINIOS_EMAIL)
    numero = random.randint(1, 999)
    return f"{base}{numero}@{dominio}"

def _telefone_aleatorio() -> str:
    ddd = random.choice([11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 31, 41, 51, 61, 71, 81])
    parte1 = random.randint(90000, 99999)
    parte2 = random.randint(1000, 9999)
    return f"({ddd}) {parte1}-{parte2}"

def _data_aleatoria(dias_max: int = 365) -> datetime:
    dias_atras = random.randint(0, dias_max)
    return datetime.now() - timedelta(days=dias_atras)

def gerar_clientes_simulados(quantidade: int = 50) -> List[Dict[str, Any]]:
    clientes = []
    emails_usados = set()
    
    for _ in range(quantidade):
        nome = _nome_aleatorio()
        email = _email_aleatorio(nome)
        while email in emails_usados:
            email = _email_aleatorio(nome + str(random.randint(1, 99)))
        emails_usados.add(email)
        
        cliente = {
            "nome": nome,
            "email": email,
            "telefone": _telefone_aleatorio(),
            "data_cadastro": _data_aleatoria(dias_max=365) 
        }
        clientes.append(cliente)
    
    return clientes

def gerar_interacoes_simuladas(
    clientes_ids: List[int],
    quantidade: int = 150
) -> List[Dict[str, Any]]:
    interacoes = []
    
    for _ in range(quantidade):
        cliente_id = random.choice(clientes_ids)
        tipo = random.choice(TIPOS_INTERACAO)
        descricao_base = random.choice(DESCRICOES_POR_TIPO[tipo])
        
        if tipo == "ligacao":
            duracao = random.randint(2, 45)
            descricao = f"{descricao_base} (duração: {duracao} min)"
        elif tipo == "email":
            anexo = random.choice(["nenhum", "PDF", "DOCX", "XLSX"])
            descricao = f"{descricao_base} Anexo: {anexo}."
        elif tipo == "whatsapp":
            midia = random.choice(["texto", "áudio", "imagem", "vídeo curto"])
            descricao = f"{descricao_base} Tipo de mídia: {midia}."
        else:
            descricao = descricao_base
        
        interacao = {
            "cliente_id": cliente_id,
            "tipo": tipo,
            "descricao": descricao,
            "data": _data_aleatoria(dias_max=180)  
        }
        interacoes.append(interacao)
    
    return interacoes