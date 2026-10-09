from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from typing import Generic, TypeVar

from sqlalchemy import case
from sqlalchemy.orm import Session

from app.enums import CampoOrdenacao, Ordem, PrioridadeTarefa, StatusTarefa
from app.models import Tarefa, Usuario

Entidade = TypeVar("Entidade")

class RepositorioBase(ABC, Generic[Entidade]):
    def __init__(self, sessao: Session):
        self._sessao = sessao
    @property
    @abstractmethod
    def modelo(self) -> TypeVar[Entidade]:
        """Classe abstrata do modelo de administração do repositorio"""
    def Buscar_por_id(self, id : int) -> Entidade | None:
        return self._sessao.get(self.modelo, id)
    def salvar(self, entidade: Entidade) -> Entidade:
        self._sessao.add(entidade)
        self._sessao.commit()
        self._sessao.refresh(entidade)
        return entidade
    def remover(self, entidade :Entidade) -> None:
        self._sessao.delete(entidade)
        self._sessao.commit()
class UsuarioRepositorio(RepositorioBase[Usuario]):
    @property
    def modelo(self) -> TypeVar[Usuario]:
        return Usuario
    def Buscar_por_email(self, email: str) -> Usuario | None:
        return (
            self._sessao.query(Usuario).filter(
                Usuario.email == email.strip().lower()).first())
    def email_existe( self, email: str) -> bool:
        return self.Buscar_por_email(email) is not None

@dataclass(frozen=True)
class FiltroTarefas:
    usuario_id :int
    status: StatusTarefa | None = None
    prioridade: PrioridadeTarefa | None = None
    prazo_ate: date | None = None
    ordenar_por: CampoOrdenacao = CampoOrdenacao.CRIADO_EM
    ordem: Ordem = Ordem.DESC
    limite: int = 50
    deslocamento = int = 0
class TarefaRepositorio(RepositorioBase[Tarefa]):
    _ORDEM_POR_PRIORIDADE = case(
        PrioridadeTarefa.mapa_de_pesos(), value=Tarefa.prioridade, else_=99
    )
    def modelo(self) -> type[Tarefa]:
        return Tarefa
    def _coluna_de_ordenacao (self, campo: CampoOrdenacao):
        colunas = {
            CampoOrdenacao.CRIADO_EM: Tarefa.criado_em,
            CampoOrdenacao.PRAZO: Tarefa.prazo,
            CampoOrdenacao.PRIORIDADE: self._ORDEM_POR_PRIORIDADE,
        } 
        return colunas[campo]
    def listar(self, filtro: FiltroTarefas) -> list[Tarefa]:
        consulta = self._sessao.query(Tarefa).filter(
            Tarefa.usuario_id == filtro.usuario_id
        )
        if filtro.status is not None:
            consulta = consulta.filter(
                Tarefa.status == filtro.status.value
            )
        if filtro.prioridade is not None:
            consulta = consulta.filter(
                Tarefa.prioridade == filtro.prioridade.value
            ) 
        if filtro.prazo_ate is not None:
            consulta = consulta.filter(
                Tarefa.prazo != None, Tarefa.prazo <= filtro.prazo_ate
            ) 
        coluna = self._coluna_de_ordenacao(filtro.ordenar_por)
        consulta = consulta.order_by(coluna.desc()
                                     if filtro.ordem is Ordem.DESC
                                     else coluna.asc())
        return(consulta.offset(filtro.deslocamento)
               .limit(filtro.limite).all())