class ErroDoDominio(Exception):
    mensagem = "Não foi possivel concluir sua operação"
    def __init__(self, mensagem: str | None = None) -> None:
        self.mensagem = mensagem or type(self).mensagem
class RecursoNaoEncontrado(ErroDoDominio): mensagem= "Recurso não encontrado"
class UsuarioNaoEncontrado(RecursoNaoEncontrado): mensagem = "Usuario não encontrado"
class TarefaNaoEncontrada(RecursoNaoEncontrado): mensagem = "Tarefa não encontrada"
class RegraDeNegocioViolada(ErroDoDominio): 
    mensagem = "Operação recusada por um regra do software"
class TituloObrigatorio(RegraDeNegocioViolada):
    mensagem = "O Titulo da tarefa é obrigatorio"
class ValorInvalido(RegraDeNegocioViolada):
    mensagem = "O valor inserido é invalido"
class EmailJaCadastrado(ErroDoDominio): mensagem = "E-mail ja Cadastrado"
class CredenciaisInvalidas(ErroDoDominio): mensagem = "E-mail ou senha invalidos."
class AcessoNaoAutorizado(ErroDoDominio):
    mensagem = "Você não possui permissão para Acessar esse recurso"
