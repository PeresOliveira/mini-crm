from fastapi import status

def test_create_interacao_success(client, sample_cliente_data, sample_interacao_data):
    """Criar interação para cliente existente"""
    # Criar cliente
    cliente_resp = client.post("/clientes/", json=sample_cliente_data)
    cliente_id = cliente_resp.json()["id"]
    # Criar interação
    interacao_data = sample_interacao_data.copy()
    interacao_data["cliente_id"] = cliente_id
    response = client.post("/interacoes/", json=interacao_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["tipo"] == sample_interacao_data["tipo"]
    assert data["descricao"] == sample_interacao_data["descricao"]
    assert data["cliente_id"] == cliente_id
    assert "id" in data
    assert "data" in data

def test_create_interacao_cliente_inexistente(client, sample_interacao_data):
    """Tentar criar interação para cliente que não existe deve dar 404"""
    interacao_data = sample_interacao_data.copy()
    interacao_data["cliente_id"] = 99999
    response = client.post("/interacoes/", json=interacao_data)
    assert response.status_code == 404
    assert "não encontrado" in response.json()["detail"]

def test_create_interacao_tipo_invalido(client, sample_cliente_data):
    """Tipo de interação inválido deve retornar 422"""
    cliente_resp = client.post("/clientes/", json=sample_cliente_data)
    cliente_id = cliente_resp.json()["id"]
    interacao_invalida = {
        "cliente_id": cliente_id,
        "tipo": "tipo_invalido",
        "descricao": "teste"
    }
    response = client.post("/interacoes/", json=interacao_invalida)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_list_interacoes_cliente(client, sample_cliente_data, sample_interacao_data):
    # Criar cliente
    cliente_resp = client.post("/clientes/", json=sample_cliente_data)
    cliente_id = cliente_resp.json()["id"]
    # Criar duas interações
    interacao1 = sample_interacao_data.copy()
    interacao1["cliente_id"] = cliente_id
    interacao1["tipo"] = "ligacao"
    interacao2 = sample_interacao_data.copy()
    interacao2["cliente_id"] = cliente_id
    interacao2["tipo"] = "email"
    client.post("/interacoes/", json=interacao1)
    client.post("/interacoes/", json=interacao2)
    # Listar
    response = client.get(f"/interacoes/cliente/{cliente_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    tipos = [item["tipo"] for item in data]
    assert "ligacao" in tipos
    assert "email" in tipos

def test_list_interacoes_paginacao(client, sample_cliente_data):
    """Teste de paginação nas interações"""
    cliente_resp = client.post("/clientes/", json=sample_cliente_data)
    cliente_id = cliente_resp.json()["id"]
    # Criar 10 interações
    for i in range(10):
        client.post("/interacoes/", json={
            "cliente_id": cliente_id,
            "tipo": "whatsapp",
            "descricao": f"Interação {i}"
        })
    # Buscar skip=3 limit=4
    response = client.get(f"/interacoes/cliente/{cliente_id}?skip=3&limit=4")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 4

def test_list_interacoes_filtro_tipo(client, sample_cliente_data):
    """Filtrar interações por tipo"""
    cliente_resp = client.post("/clientes/", json=sample_cliente_data)
    cliente_id = cliente_resp.json()["id"]
    # Criar interações de diferentes tipos
    client.post("/interacoes/", json={"cliente_id": cliente_id, "tipo": "ligacao", "descricao": "Ligação 1"})
    client.post("/interacoes/", json={"cliente_id": cliente_id, "tipo": "email", "descricao": "Email 1"})
    client.post("/interacoes/", json={"cliente_id": cliente_id, "tipo": "ligacao", "descricao": "Ligação 2"})
    # Filtrar por ligacao
    response = client.get(f"/interacoes/cliente/{cliente_id}?tipo=ligacao")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    for item in data:
        assert item["tipo"] == "ligacao"

def test_get_interacao_by_id(client, sample_cliente_data, sample_interacao_data):
    cliente_resp = client.post("/clientes/", json=sample_cliente_data)
    cliente_id = cliente_resp.json()["id"]
    interacao_data = sample_interacao_data.copy()
    interacao_data["cliente_id"] = cliente_id
    create_resp = client.post("/interacoes/", json=interacao_data)
    interacao_id = create_resp.json()["id"]
    response = client.get(f"/interacoes/{interacao_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == interacao_id
    assert data["cliente_id"] == cliente_id

def test_get_interacao_not_found(client):
    """Buscar interação inexistente retorna 404"""
    response = client.get("/interacoes/99999")
    assert response.status_code == 404

def test_update_interacao_success(client, sample_cliente_data, sample_interacao_data):
    """Atualizar interação existente"""
    cliente_resp = client.post("/clientes/", json=sample_cliente_data)
    cliente_id = cliente_resp.json()["id"]
    interacao_data = sample_interacao_data.copy()
    interacao_data["cliente_id"] = cliente_id
    create_resp = client.post("/interacoes/", json=interacao_data)
    interacao_id = create_resp.json()["id"]
    update_data = {"descricao": "Nova descrição atualizada", "tipo": "email"}
    response = client.put(f"/interacoes/{interacao_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["descricao"] == "Nova descrição atualizada"
    assert data["tipo"] == "email"

def test_update_interacao_not_found(client):
    response = client.put("/interacoes/99999", json={"descricao": "teste"})
    assert response.status_code == 404

def test_delete_interacao_success(client, sample_cliente_data, sample_interacao_data):
    """Deletar interação existente"""
    cliente_resp = client.post("/clientes/", json=sample_cliente_data)
    cliente_id = cliente_resp.json()["id"]
    interacao_data = sample_interacao_data.copy()
    interacao_data["cliente_id"] = cliente_id
    create_resp = client.post("/interacoes/", json=interacao_data)
    interacao_id = create_resp.json()["id"]
    response = client.delete(f"/interacoes/{interacao_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    # Verificar que sumiu
    get_resp = client.get(f"/interacoes/{interacao_id}")
    assert get_resp.status_code == 404

def test_estatisticas_interacoes(client, sample_cliente_data):
    """Endpoint de estatísticas deve retornar totais por tipo"""
    cliente_resp = client.post("/clientes/", json=sample_cliente_data)
    cliente_id = cliente_resp.json()["id"]
    # Criar interações
    client.post("/interacoes/", json={"cliente_id": cliente_id, "tipo": "ligacao", "descricao": "L1"})
    client.post("/interacoes/", json={"cliente_id": cliente_id, "tipo": "ligacao", "descricao": "L2"})
    client.post("/interacoes/", json={"cliente_id": cliente_id, "tipo": "email", "descricao": "E1"})
    response = client.get(f"/interacoes/cliente/{cliente_id}/estatisticas")
    assert response.status_code == 200
    data = response.json()
    assert data["cliente_id"] == cliente_id
    assert data["total_interacoes"] == 3
    assert data["detalhes_por_tipo"]["ligacao"] == 2
    assert data["detalhes_por_tipo"]["email"] == 1