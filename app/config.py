from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()
RAIZ_PROJETO = Path(__file__).resolve().parent.parent
CAMINHO_ENV = RAIZ_PROJETO / ".env"
ENV_ENCONTRADO = load_dotenv(CAMINHO_ENV)

#remover futuramente
ORIGENS_PADRAO = (
    "http://localhost:5173"
)

def normalizar_url(url: str) -> str:
    url = url.strip()
    if url.startswith("postgres://"):
        return "postgresql+psycopg://" + url[len("postgres://"):]
    if url.startswith("postgresql://"):
        return "postgresql+psycopg://" + url[len("postgresql://"):]
    return url

@dataclass(frozen=True)
class Configuracao:
    url_banco: str
    origens: tuple[str, ...] = ORIGENS_PADRAO
    echo_sql : bool = False
    @classmethod
    def do_ambiente(cls) -> Configuracao:
        banco_de_dados_url = os.getenv("DATABASE_URL", "").strip()
        if not banco_de_dados_url:
            raise RuntimeError(
                "A variavel de ambiente DATABASE_URL não foi definida \n"
                f"Esperado um arquivo .env em {CAMINHO_ENV}\n"
                f"Arquivo encontrado: {'sim' if ENV_ENCONTRADO else 'não'}"
            )
        origens = os.getenv("ORIGENS_PERMITIDADAS", "").strip()
        origens_permitidas = (
            tuple(
                origem.strip()
                for origem in origens.split(",")
                if origem.strip()
            )
            # remover na proxima entrega
            or ORIGENS_PADRAO
        ) 
        echo_sql = os.getenv("ECHO_SQL", "").strip().lower() in {
            "1",
            "true",
            "sim",
            "yes"
        } 
        return cls(
            url_banco = normalizar_url(banco_de_dados_url),
            origens=origens_permitidas,
            echo_sql = echo_sql
        )
    @property
    def dialeto(self) -> str:
        return self.url_banco.split(":",1)[0].split("+",1)[0]
    @property
    def banco_em_memoria(self) -> bool:
        return self.dialeto == "sqlite" and (
            ":memory:" in self.url_banco
            or self.url_banco == "sqlite://")
    @property 
    def banco_em_servidor(self) -> bool:
        return self.dialeto != "sqlite"
@lru_cache
def obter_configuracao() -> Configuracao:
    return Configuracao.do_ambiente()