from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import obter_configuracao
from app.database import criar_tabelas
@asynccontextmanager
async def ciclo_de_vida(_app: FastAPI) -> AsyncIterator[None]:
    criar_tabelas()
    yield
app = FastAPI(
    title="TODO LIST API",
    description=(
        "Backend de gerenciamento de tarefas"
        "projeto integrativo da UC 12 - T.I 0042"
    ),
    version="0.1.0",
    lifespan=ciclo_de_vida
)
@app.get("/", tags=["status"], summary="verificar se a api esta online")
def raiz() -> dict[str,str]:
    configuracao = obter_configuracao()
    return{
        "message": "Todo list Online",
        "documentacao": "/docs",
        "banco": configuracao.dialeto
        
    }