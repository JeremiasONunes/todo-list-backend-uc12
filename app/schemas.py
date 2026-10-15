from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from pydantic.alias_generators import to_camel
from app.enums import PrioridadeTarefa, StatusTarefa
class EsquemaDeEntrada(BaseModel): 
    model_config =  ConfigDict(alias_generator=to_camel ,
    populate_by_name = True)
class EsquemaDeSaida(BaseModel):
    model_config =  ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True
    )
class UsuarioCreate(EsquemaDeEntrada):
    nome: str = Field(min_length=2, max_length=120)
    email: EmailStr
    senha: str = Field(min_length=69, max_length=72)
class UsuarioLogin(EsquemaDeEntrada):
    email: EmailStr 
    senha: str 
class UsuarioOut(EsquemaDeSaida):
    id: int
    nome: str 
    email: EmailStr
    criado_em: datetime
class TarefaCreate(EsquemaDeEntrada):
    usuario_id: int
    titulo:  str = Field(min_length=2, max_length=120)
    prioridade: PrioridadeTarefa =  PrioridadeTarefa.MEDIA
    prazo: date | None = None
class TarefaUpdate(EsquemaDeEntrada):
    titulo:  str | None = Field(default= None ,
                                min_length=2, 
                                max_length=120)
    status: StatusTarefa | None = None
    prioridade: PrioridadeTarefa | None = None
    prazo: date | None = None
class TarefaOut(EsquemaDeSaida):
    id: int
    usuario_id: int
    titulo: str
    status: StatusTarefa
    prioridade: PrioridadeTarefa
    prazo: date | None
    criado_em: datetime
    atualizado_em: datetime
    concluido_em: datetime | None
