from enum import Enum
from uuid import UUID, uuid4

from fastapi import FastAPI
from pydantic import BaseModel, constr

app = FastAPI()

TAREFAS = [
    {
        "id": 1,
        "titulo": "Fazer compras",
        "descrição": "Ir ao super",
        "estado": "não finalizado",
    }
]


@app.get("/tarefas")
def listar():
    return TAREFAS


class EstadosPossiveis(str, Enum):
    finalizado = "finalizado"
    nao_finalizado = "não finalizado"


class TarefaEntrada(BaseModel):
    titulo: constr(min_length=3, max_length=50)
    descricao: constr(max_length=140)
    estado = EstadosPossiveis = EstadosPossiveis.nao_finalizado


class Tarefa(TarefaEntrada):
    id: UUID


@app.post("/tarefas", response_model=Tarefa, status_code=201)
def criar(tarefa: TarefaEntrada):
    nova_tarefa = tarefa.dict()
    nova_tarefa.update({"id": uuid4()})
    TAREFAS.append(nova_tarefa)
    return nova_tarefa
