from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import obter_sessao
from app.repositories import TarefaRepositorio, UsuarioRepositorio
from app.security import HashBcrypt, HashDeSenha
from app.services import TarefaServicos, UsuarioServicos

def obter_hash() -> HashDeSenha:
    return HashBcrypt()
def obter_usuario_servico(
    sessao: Session = Depends(obter_sessao),
    hasher: HashDeSenha = Depends(obter_hash),
) -> UsuarioServicos:
    return UsuarioServicos(UsuarioRepositorio(sessao), hasher)
def obter_tarefa_servico(
    sessao: Session =  Depends(obter_sessao),
)-> TarefaServicos:
    return TarefaServicos(TarefaRepositorio(sessao), UsuarioRepositorio(sessao))