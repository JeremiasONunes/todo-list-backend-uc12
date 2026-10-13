from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any

from app.enums import PrioridadeTarefa, StatusTarefa
from app.exceptions import (
    CredenciaisInvalidas,
    EmailJaCadastrado,
    TarefaNaoEncontrada,
    UsuarioNaoEncontrado
)
from app.models import Tarefa , Usuario
from app.repositories import FiltroTarefas,TarefaRepositorio,UsuarioRepositorio
from app.security import HashDeSenha

NAO_INFORMADO: Any = object()

@dataclass(frozen=True)
class AlteracoesDaTarefa:
    titulo: Any = NAO_INFORMADO
    status: Any = NAO_INFORMADO
    prioridade: Any = NAO_INFORMADO
    prazo: Any = NAO_INFORMADO
    
    def informado(self, campo: str) -> bool:
        return getattr(self,campo) is not NAO_INFORMADO

class UsuarioService:
    def __init__(self, repositorio: UsuarioRepositorio, Hasher: HashDeSenha) -> None:
        self._repositorio = repositorio
        self._hasher = Hasher
    def cadastrar(self, nome: str, email: str, senha: str) -> Usuario:
        if self._repositorio.email_existe(email):
            raise EmailJaCadastrado
        usuario = Usuario(nome=nome, email=email)
        usuario.definir_senha(senha, self._hasher)
        return self._repositorio.salvar(usuario)
    def autenticar(self, email:str, senha:str) -> Usuario:
        usuario = self._repositorio.Buscar_por_email(email)
        if usuario is None or not usuario.senha_confere(senha, self._hasher):
            raise CredenciaisInvalidas()
        return usuario
    def buscar(self, usuario_id: int) -> Usuario:
        usuario = self._repositorio.Buscar_por_id(usuario_id)
        if usuario is None:
            raise UsuarioNaoEncontrado()
        return usuario
class TarefaServicos:
    def __init__(
        self, tarefa: TarefaRepositorio, usuario: UsuarioRepositorio
    ) -> None:
        self._tarefa = tarefa
        self._usuario = usuario
        
    def criar (
        self, usuario_id: int, 
        titulo: str, 
        prioridade: PrioridadeTarefa, 
        prazo: date | None) -> Tarefa:
        
        if self._usuario.Buscar_por_id(usuario_id) is None:
            raise UsuarioNaoEncontrado()
        tarefa = Tarefa(
            usuario_id=usuario_id,
            titulo=titulo,
            prioridade=prioridade,
            prazo=prazo)
        return self._tarefa.salvar(tarefa)
    def atualizar(self, tarefa_id: int, alteracoes: AlteracoesDaTarefa) -> Tarefa:
        tarefa = self._tarefa.Buscar_por_id(tarefa_id)
        
        if tarefa is None: 
            raise TarefaNaoEncontrada()
        if alteracoes.informado("titulo"):
            tarefa.titulo = alteracoes.titulo
        if alteracoes.informado("prioridade"):
            tarefa.prioridade = alteracoes.prioridade
        if alteracoes.informado("prazo"):
            tarefa.prazo = alteracoes.prazo
        if alteracoes.informado("status"):
            tarefa.definir_status(StatusTarefa(alteracoes.status))
        return self._tarefa.salvar(tarefa)
    def remover(self, tarefa_id: int) -> None:
        tarefa = self._tarefa.Buscar_por_id(tarefa_id)
        if tarefa is not None: 
            self._tarefa.remover(tarefa)
        else:
           raise TarefaNaoEncontrada()
    def listar(self, filtro:FiltroTarefas)-> list[Tarefa]:
        return self._tarefa.listar(filtro)
        
       
    