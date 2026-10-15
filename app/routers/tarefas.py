from datetime import date
from typing import Annotated
from fastapi import APIRouter, Depends,Query, Response ,status
from app.dependencies import obter_tarefa_servico
from app.enums import CampoOrdenacao,Ordem,PrioridadeTarefa,StatusTarefa
from app.repositories import FiltroTarefas
from app.schemas import TarefaCreate,TarefaUpdate, TarefaOut
from app.services import AlteracoesDaTarefa, TarefaServicos
router = APIRouter(prefix="/tarefas", tags=["Tarefas"])
@router.post(
    "",
    response_model=TarefaOut,
    status_code=status.HTTP_201_CREATED,
    summary= "Criar tarefa",
    responses={404: {"description": "Usuario nao encontrado!"}},
)
def criar_tarefa(
    dados: TarefaCreate,
    servico: Annotated[TarefaServicos, 
                       Depends(obter_tarefa_servico)],
)-> TarefaOut:
    return servico.criar(
        usuario_id=dados.usuario_id,
        titulo=dados.titulo,
        prioridade=dados.prioridade,
        prazo=dados.prazo
    )
def _montar_alteracoes(dados: TarefaUpdate) -> AlteracoesDaTarefa:
    return AlteracoesDaTarefa(**dados.model_dump(exclude_unset=True))
@router.patch(
    "/{tarefa_id}",
    response_model=TarefaOut,
    summary= "Atualizar tarefa",
    responses={404: {"description": "Tarefa nao encontrado!"}},
)
def atulizar_tarefa(
    tarefa_id: int,
    dados: TarefaUpdate,
    servico: Annotated[TarefaServicos, 
                       Depends(obter_tarefa_servico)],
)-> TarefaOut:
    return servico.atualizar(tarefa_id, _montar_alteracoes(dados))

@router.delete(
    "/{tarefa_id}",
    status_code= status.HTTP_204_NO_CONTENT,
    summary= "deletar tarefa",
    responses={404: {"description": "Tarefa nao encontrado!"}},
)
def remover_tarefa(
    tarefa_id: int,
    servico: Annotated[TarefaServicos, 
                       Depends(obter_tarefa_servico)],
)-> Response:
    servico.remover(tarefa_id)
    return Response(status_code= status.HTTP_204_NO_CONTENT)

@router.get(
    "",
    response_model=list[TarefaOut],
    summary= "listar tarefa",
)
def listar_tarefa(
    servico: Annotated[TarefaServicos, 
                       Depends(obter_tarefa_servico)],
    usuario_id : Annotated[
        int, Query(alias="usuario_id", description="ID do usuario")
    ],
    status_tarefa: Annotated[
        StatusTarefa | None, Query(alias="status")
    ] = None,
    prioridade: Annotated[
        PrioridadeTarefa | None, Query()
    ] = None,
    prazo_ate: Annotated[
        date | None, Query(alias="prazoAte" , 
        description="somente tarefas com o prazo até está data")
    ] = None,
    ordem: Annotated[Ordem, Query()] = Ordem.DESC,
    limite: Annotated[int, Query(ge=1, le=200, alias="limit")] = 50,
    deslocamento: Annotated[int, Query(ge=0, alias="offset")] = 0,
    ordenar_por: Annotated[CampoOrdenacao, 
                Query(alias="ordenarPor")] = CampoOrdenacao.CRIADO_EM,
)-> list[TarefaOut]:
    filtro = FiltroTarefas(
        usuario_id=usuario_id,
        status=status_tarefa,
        prioridade=prioridade,
        prazo_ate=prazo_ate,
        ordem=ordem,
        limite=limite,
        deslocamento=deslocamento,
        ordenar_por=ordenar_por
    )
    return servico.listar(filtro)