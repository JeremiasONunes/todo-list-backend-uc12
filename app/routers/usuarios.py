from typing import Annotated
from fastapi import APIRouter, Depends, status

from app.dependencies import obter_usuario_servico
from app.services import UsuarioServicos
from app.schemas import UsuarioCreate, UsuarioLogin, UsuarioOut

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary= "Cadastrar usuário",
    responses={409: {"description": "E-mail ja cadastrado"}},
)
def cadastrar_usuario(
    dados: UsuarioCreate,
    servico: Annotated[UsuarioServicos, 
                       Depends(obter_usuario_servico)],
)-> UsuarioOut:
    return servico.cadastrar(dados.nome , dados.email, dados.senha)

@router.post(
    "/login",
    response_model=UsuarioOut,
    summary= "Autenticar usuário",
    responses={401: {"description": "E-mail ou Senha invalidos"}},
)
def autenticar_usuario(
    dados: UsuarioLogin,
    servico: Annotated[UsuarioServicos, 
                       Depends(obter_usuario_servico)],
)-> UsuarioOut:
    return servico.autenticar(dados.email, dados.senha)
@router.get(
    "/{usuario_id}",
    response_model=UsuarioOut,
    summary= "Consultar usuário",
    responses={404: {"description": "Usuário não encontrado"}},
)
def buscar_usuario(
    usuario_id: int,
    servico: Annotated[UsuarioServicos, 
                       Depends(obter_usuario_servico)],
)-> UsuarioOut:
    return servico.buscar(usuario_id)
