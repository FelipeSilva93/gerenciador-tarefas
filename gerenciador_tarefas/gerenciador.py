from fastapi import FastAPI

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
