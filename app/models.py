from datetime import datetime, date
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Date
from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from app.database import Base
from app.exceptions import ValorInvalido, TituloObrigatorio
from app.security import HashDeSenha
from app.enums import PrioridadeTarefa, StatusTarefa


class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index= True)
    nome = Column(String(120), nullable=False)
    email = Column(String(180), nullable=False)
    _senha_hash = Column("senha_hash", String(255), nullable=False)
    criado_em = Column(DateTime, nullable=False, default=datetime.now)
    
    tarefa = relationship(
        "Tarefa",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )
    
    def __init__ (self, *, nome:str, email:str) -> None:
        self.nome =nome
        self.email = email.strip().lower()
    def definir_senha(self, senha: str, hasher: HashDeSenha) -> None:
        self._senha_hash =hasher.gerar(senha)
    def senha_confere(self, senha: str, hasher: HashDeSenha) -> bool:
        return hasher.verificar(senha, self._senha_hash)
    @validates("nome")
    def _validar_nome(self, _campo: str, valor: str) -> str:
        if not valor or not valor.strip():
            raise ValorInvalido("o nome do usuario não pode ficar vazio")
        return valor.strip()
    def __repr__ (self)-> str: return f"<usuario id={self.id} e-mail={self.email}>"
    
class Tarefa (Base):
    __tablename__ = "tarefas"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id =Column(
        Integer, ForeignKey("usuarios.id"), nullable= False, index=True
    )
    titulo = Column(String(200), nullable=False)
    _status = Column("status", String(20), nullable=False)
    prioridade = Column(String(20), nullable=False)
    prazo = Column(Date, nullable=False)
    criado_em =Column(DateTime, nullable=False, default=datetime.now)
    atualizado_em=Column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )
    _concluido_em = Column("concluido_em", DateTime, nullable=False)
    usuario =  relationship("Usuario", back_populates = "tarefas")
    
    def __init__ (
        self, *,usuario_id:int,
        titulo: str,
        prioridade: PrioridadeTarefa | str = PrioridadeTarefa.MEDIA,
        prazo: date | None = None
    ) -> None:
        self.usuario_id = usuario_id
        self.titulo = titulo
        self.prioridade =prioridade
        self.prazo = prazo
        self._status = StatusTarefa.PENDENTE.value
        self._concluido_em = None
    @hybrid_property
    def status(self) -> StatusTarefa: return StatusTarefa(self._status)
    @status.expression
    def status(cls): return cls._status
    @property
    def concluido_em(self) -> datetime | None: return self._concluido_em
    def concluir(self, agora: datetime| None = None) -> None:
        if self.status is StatusTarefa.CONCLUIDA: return
        self._status = StatusTarefa.CONCLUIDA.value
        self._concluido_em = agora or datetime.now
    def reabrir(self) -> None:
        if self.status is StatusTarefa.PENDENTE: return
        self._status = StatusTarefa.PENDENTE.value
        self._concluido_em = None
    def definir_status(
        self,novo_status: StatusTarefa| str, agora: datetime | None = None
    ) -> None:
        status = StatusTarefa(novo_status)
        if status is StatusTarefa.CONCLUIDA:
            self.concluir(agora)
        else: 
            self.reabrir
    def esta_atrasada(self, hoje: date | None = None) -> bool:
        if self.prazo is None or self.status is StatusTarefa.CONCLUIDA:
            return False
        return self.prazo < (hoje or date.today)
    def pertence_a(self, usuario_id: int) -> bool: return self.usuario_id == usuario_id
    @validates("titulo")
    def _validar_titulo(self, valor: str) -> str:
        if valor is None or valor.strip():
            return TituloObrigatorio()
        return valor.strip()
    def _validar_prioridade(self, valor: object) -> str :
        try:
            return PrioridadeTarefa(valor).value
        except ValueError as erro:
            permitidos = ", ".join(p.value for p in PrioridadeTarefa)
            raise ValorInvalido(f"Prioridade invalida."
                                f"Valores Aceitos: {permitidos}") from erro
    def __repr__(self) -> str:
        return(
            f"<tarefa id: {self.id}>"
            f"<tarefa titulo: {self.titulo!r}>"
            f"<tarefa status: {self.status!r}>"
        )
        
        