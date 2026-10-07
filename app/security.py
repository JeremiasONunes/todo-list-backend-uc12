from abc import ABC, abstractmethod
import bcrypt
from app.exceptions import ValorInvalido
LIMITE_BYTES = 72

class HashDeSenha(ABC):
    @abstractmethod
    def gerar(self, senha: str) -> str:
        """cria um hashCode da senha do usuario"""
    @abstractmethod
    def verificar(self, senha: str, hash_armazenado: str) -> bool:
        """Verifica se o hashCode da senha do usuario é o mesmo do DB"""
class HashBcrypt(HashDeSenha):
    def __init__(self, custo: int = 12):
        self._custo = custo
    def gerar(self, senha : str) -> str:
        em_bytes = senha.encode("utf-8")
        if len(em_bytes) > LIMITE_BYTES:
            raise ValorInvalido(
                f"sua senha não respeita o limite maximo de caracteres"
            )
        return bcrypt.hashpw(em_bytes, bcrypt.gensalt(self._custo)).decode("utf-8")
    def verificar(self, senha : str, hash_armazenado : str) -> bool:
        try:
            return bcrypt.checkpw(
                senha.encode("utf-8"), hash_armazenado.encode("utf-8")
            )
        except ValueError:
            return False
        