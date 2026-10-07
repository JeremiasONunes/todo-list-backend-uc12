from __future__ import annotations
import sqlite3
from collections.abc import Generator
from typing import Any
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool

from app.config import Configuracao, obter_configuracao

def _opcoes_do_engine(configuracao: Configuracao) -> dict[str, Any]:
    if configuracao.banco_em_memoria and configuracao.dialeto == "sqlite":
        opcoes: dict[str, Any] = {"connect_args": {"check_same_thread": False}}
        opcoes["poolclass"] = StaticPool
        return opcoes
    return {"pool_pre_ping": True, "pool_recycle": 1000}

@event.listens_for(Engine,"connect")
def _ativar_chaves_estrangeiras(conexao_dbapi:Any, registro:Any) -> None:
    if isinstance(conexao_dbapi, sqlite3.Connection):
        cursor = conexao_dbapi.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
    
_configuracao = obter_configuracao()
engine = create_engine(
    _configuracao.url_banco,
    echo=_configuracao.echo_sql,
    **_opcoes_do_engine(_configuracao)
)

Sessao_Local = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def criar_tabelas() -> None:
    Base.metadata.create_all(bind=engine)
def obter_sessao() -> Generator[Session, None,None]:
    sessao = Sessao_Local()
    try:
        yield sessao
    finally:
        sessao.close
        
