from enum import Enum

class StatusTarefa(str,Enum):
    PENDENTE = "pendente"
    CONCLUIDA = "concluida"

class PrioridadeTarefa(str, Enum):
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"
    URGENTE = "urgente"
    
    @property
    def peso(self) -> int:
        return _PESOS[self]
    @classmethod
    def mapa_de_pesos(cls) ->dict[str, int] :
        return {prioridade.value: prioridade.peso for prioridade in cls}
_PESOS = {
    PrioridadeTarefa.URGENTE: 0,
    PrioridadeTarefa.ALTA: 1,
    PrioridadeTarefa.MEDIA: 2,
    PrioridadeTarefa.BAIXA: 3
}
class CampoOrdenacao(str, Enum):
    CRIADO_EM  = "criadoEm"
    PRAZO = "prazo"
    PRIORIDADE = "Prioridade"   
class Ordem(str, Enum):
    ASC= "asc"
    DESC= "desc" 