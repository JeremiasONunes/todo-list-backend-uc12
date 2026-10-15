from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import obter_configuracao
from app.database import criar_tabelas
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import Request
from app.exceptions import(
    AcessoNaoAutorizado,
    CredenciaisInvalidas,
    EmailJaCadastrado,
    ErroDoDominio,
    RecursoNaoEncontrado,
    RegraDeNegocioViolada
)
STATUS_POR_ERRO: tuple[tuple[type[ErroDoDominio], int], ...] = (
    (RecursoNaoEncontrado, 404),
    (EmailJaCadastrado, 409),
    (CredenciaisInvalidas, 401),
    (AcessoNaoAutorizado, 403),
    (RegraDeNegocioViolada, 422),
    (ErroDoDominio, 400),
)
from app.routers import usuarios, tarefas
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
    version="2.1.0",
    lifespan=ciclo_de_vida
)
app.include_router(usuarios.router)
app.include_router(tarefas.router)

@app.get("/", tags=["status"], summary="verificar se a api esta online")
def raiz() -> dict[str,str]:
    configuracao = obter_configuracao()
    return{
        "message": "Todo list Online",
        "documentacao": "/docs",
        "banco": configuracao.dialeto
        
    }