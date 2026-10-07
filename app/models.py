from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import validates
from app.database import Base
from app.exceptions import ValorInvalido
from app.security import HashDeSenha

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index= True)
    nome = Column(String(120), nullable=False)
    email = Column(String(180), nullable=False)
    _senha_hash = Column("senha_hash", String(255), nullable=False)
    criado_em = Column(DateTime, nullable=False, default=datetime.now)
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
        