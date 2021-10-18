from fastapi import status
from fastapi.testclient import TestClient
from gerenciador_tarefas.gerenciador import TAREFAS, app


def test_quando_listar_tarefas_devo_ter_retorno_codigo_status_200():
    cliente = TestClient(app)
    resposta = cliente.get("/tarefas")
    assert resposta.status_code == status.HTTP_200_OK
    TAREFAS.clear()


def test_quando_listar_tarefas_formato_de_retorno_deve_ser_json():
    cliente = TestClient(app)
    resposta = cliente.get("/tarefas")
    assert resposta.headers["content-type"] == "application/json"
    TAREFAS.clear()


def test_quando_listar_tarefas_retorno_deve_ser_uma_lista():
    cliente = TestClient(app)
    resposta = cliente.get("/tarefas")
    assert isinstance(resposta.json(), list)
    TAREFAS.clear()


def test_quando_listar_tarefas_a_tarefa_retornada_deve_possuir_id():
    TAREFAS.append({"id": 1})
    cliente = TestClient(app)
    resposta = cliente.get("/tarefas")
    assert "id" in resposta.json().pop()
    TAREFAS.clear()


def test_quando_listar_tarefas_a_tarefa_retornada_deve_possuir_titulo():
    TAREFAS.append({"titulo": "titulo 1"})
    cliente = TestClient(app)
    resposta = cliente.get("/tarefas")
    assert "titulo" in resposta.json().pop()
    TAREFAS.clear()


def test_quando_listar_tarefas_a_tarefa_retornada_deve_possuir_descrição():
    TAREFAS.append({"descrição": "descrição 1"})
    cliente = TestClient(app)
    resposta = cliente.get("/tarefas")
    assert "descrição" in resposta.json().pop()
    TAREFAS.clear()


def test_quando_listar_tarefas_a_tarefa_retornada_deve_possuir_estado():
    TAREFAS.append({"estado": "finalizado"})
    cliente = TestClient(app)
    resposta = cliente.get("/tarefas")
    assert "estado" in resposta.json().pop()
    TAREFAS.clear()


def test_recurso_tarefas_deve_aceitar_o_metodo_post():
    cliente = TestClient(app)
    resposta = cliente.post("/tarefas")
    assert resposta.status_code != status.HTTP_405_METHOD_NOT_ALLOWED
    TAREFAS.clear()


def test_quando_uma_tarefa_e_submetida_deve_possuir_um_titulo():
    cliente = TestClient(app)
    resposta = cliente.post("/tarefas", json={})
    assert resposta.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    TAREFAS.clear()


def test_titulo_da_tarefa_deve_conter_entre_3_e_50_caracteres():
    cliente = TestClient(app)
    resposta = cliente.post("/tarefas", json={"titulo": 2 * "*"})
    assert resposta.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    resposta = cliente.post("/tarefas", json={"titulo": 51 * "*"})
    assert resposta.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    TAREFAS.clear()


def test_quando_uma_tarefa_e_submetida_deve_retornar_uma_descricao():
    cliente = TestClient(app)
    resposta = cliente.post("/tarefas", json={"titulo": "titulo"})
    assert resposta.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    TAREFAS.clear()


def test_descricao_da_tarefa_pode_conter_no_maximo_140_caracteres():
    cliente = TestClient(app)
    resposta = cliente.post(
        "/tarefas", json={"titulo": "titulo", "descrição": "*" * 141}
    )
    assert resposta.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    TAREFAS.clear()


"""
def test_quando_criar_uma_tarefa_a_mesma_deve_ser_retornada():
    cliente = TestClient(app)
    tarefa = {"titulo": "titulo", "descricao": "descricao"}
    resposta = cliente.post("/tarefas", json=tarefa)
    breakpoint()
    assert resposta.json() == tarefa
"""


def test_quando_criar_uma_tarefa_seu_id_deve_ser_unico():
    cliente = TestClient(app)
    tarefa1 = {"titulo": "titulo1", "descricao": "descricao1"}
    tarefa2 = {"titulo": "titulo2", "descricao": "descricao2"}
    resposta1 = cliente.post("/tarefas", json=tarefa1)
    resposta2 = cliente.post("/tarefas", json=tarefa2)
    # breakpoint()
    assert resposta1.json()["id"] != resposta2.json()["id"]
    TAREFAS.clear()


def test_quando_criar_uma_tarefa_seu_estado_padrao_deve_ser_nao_finalizado():
    cliente = TestClient(app)
    tarefa = {"titulo": "titulo", "descricao": "descricao"}
    resposta = cliente.post("/tarefas", json=tarefa)
    assert resposta.json()["estado"] == "não finalizado"
    TAREFAS.clear()


def test_quando_criar_uma_tarefa_codigo_de_status_retornado_deve_ser_201():
    cliente = TestClient(app)
    tarefa = {"titulo": "titulo", "descricao": "descricao"}
    resposta = cliente.post("/tarefas", json=tarefa)
    assert resposta.status_code == 201
    TAREFAS.clear()


def test_quando_criar_uma_nova_tarefa_esta_deve_ser_persistida():
    cliente = TestClient(app)
    tarefa = {"titulo": "titulo", "descricao": "descricao"}
    resposta = cliente.post("/tarefas", json=tarefa)
    assert resposta.status_code == 201
    assert len(TAREFAS) == 1
    TAREFAS.clear()
