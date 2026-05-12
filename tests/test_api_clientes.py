from fastapi import status

def test_create_cliente_success(client, sample_cliente_data):
    """Teste de criação de cliente com dados válidos"""
    response = client.post("/clientes/", json=sample_cliente_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["nome"] == sample_cliente_data["nome"]
    assert data["email"] == sample_cliente_data["email"]
    assert data["telefone"] == sample_cliente_data["telefone"]
    assert "id" in data
    assert "data_cadastro" in data

def test_create_cliente_duplicate_email(client, sample_cliente_data):
    """Teste: email duplicado deve retornar 400"""
    client.post("/clientes/", json=sample_cliente_data)
    response = client.post("/clientes/", json=sample_cliente_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "já está cadastrado" in response.json()["detail"]

def test_create_cliente_invalid_email(client):
    """Teste: email inválido deve retornar 422"""
    invalid_data = {
        "nome": "Nome",
        "email": "email_invalido",
        "telefone": "123"
    }
    response = client.post("/clientes/", json=invalid_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_list_clientes_empty(client):
    """Listar clientes quando banco vazio deve retornar lista vazia"""
    response = client.get("/clientes/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

def test_list_clientes_with_data(client, sample_cliente_data):
    """Listar clientes com dados deve retornar lista não vazia"""
    client.post("/clientes/", json=sample_cliente_data)
    response = client.get("/clientes/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["email"] == sample_cliente_data["email"]

def test_list_clientes_pagination(client):
    """Teste de paginação: criar 15 clientes, buscar com skip/limit"""
    # Criar 15 clientes
    for i in range(15):
        client.post("/clientes/", json={
            "nome": f"Cliente {i}",
            "email": f"cliente{i}@teste.com",
            "telefone": "11999999999"
        })
    # Buscar skip=5, limit=5 (deve retornar 5 clientes)
    response = client.get("/clientes/?skip=5&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    # Verificar se os IDs estão corretos (ordem decrescente)
    # O primeiro da página deve ter ID 10 (se foram criados de 1 a 15)
    # Teste adicional: total de clientes deve ser 15
    response_all = client.get("/clientes/")
    assert len(response_all.json()) == 15

def test_get_cliente_by_id(client, sample_cliente_data):
    """Buscar cliente por ID existente"""
    create_response = client.post("/clientes/", json=sample_cliente_data)
    cliente_id = create_response.json()["id"]
    response = client.get(f"/clientes/{cliente_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == cliente_id
    assert data["nome"] == sample_cliente_data["nome"]

def test_get_cliente_not_found(client):
    """Buscar cliente inexistente deve retornar 404"""
    response = client.get("/clientes/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "não encontrado" in response.json()["detail"]

def test_update_cliente_success(client, sample_cliente_data):
    """Atualizar cliente com dados válidos"""
    create_resp = client.post("/clientes/", json=sample_cliente_data)
    cliente_id = create_resp.json()["id"]
    update_data = {"telefone": "11888888888", "nome": "Novo Nome"}
    response = client.put(f"/clientes/{cliente_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["telefone"] == "11888888888"
    assert data["nome"] == "Novo Nome"
    assert data["email"] == sample_cliente_data["email"]  # não alterado

def test_update_cliente_not_found(client):
    """Atualizar cliente inexistente retorna 404"""
    response = client.put("/clientes/99999", json={"nome": "Teste"})
    assert response.status_code == 404

def test_update_cliente_duplicate_email(client, sample_cliente_data):
    """Tentar atualizar email para um já existente em outro cliente"""
    client.post("/clientes/", json=sample_cliente_data)
    # Criar segundo cliente
    segundo = {
        "nome": "Segundo",
        "email": "segundo@teste.com",
        "telefone": "11999999999"
    }
    resp2 = client.post("/clientes/", json=segundo)
    segundo_id = resp2.json()["id"]
    # Tentar atualizar segundo cliente com email do primeiro
    update_data = {"email": sample_cliente_data["email"]}
    response = client.put(f"/clientes/{segundo_id}", json=update_data)
    assert response.status_code == 400
    assert "já está em uso" in response.json()["detail"]

def test_delete_cliente_success(client, sample_cliente_data):
    """Deletar cliente existente"""
    create_resp = client.post("/clientes/", json=sample_cliente_data)
    cliente_id = create_resp.json()["id"]
    response = client.delete(f"/clientes/{cliente_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    # Verificar que não existe mais
    get_resp = client.get(f"/clientes/{cliente_id}")
    assert get_resp.status_code == 404

def test_delete_cliente_not_found(client):
    """Deletar cliente inexistente retorna 404"""
    response = client.delete("/clientes/99999")
    assert response.status_code == 404

def test_estatisticas_cliente_sem_interacoes(client, sample_cliente_data):
    """Cliente sem nenhuma interação deve retornar estatísticas vazias"""
    
    cliente_resp = client.post("/clientes/", json=sample_cliente_data)
    cliente_id = cliente_resp.json()["id"]
    
    response = client.get(f"/interacoes/cliente/{cliente_id}/estatisticas")
    assert response.status_code == 200
    data = response.json()
    assert data["cliente_id"] == cliente_id
    assert data["total_interacoes"] == 0
    assert data["detalhes_por_tipo"] == {}