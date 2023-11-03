import datetime
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db.models import Q
from usuario.models import Usuario
from ..models import Pesquisa, Token


class BuscarPesquisaService:
    def __init__(self, id_usuario=None, rota=None, metodo=None):
        self.url = None
        if id_usuario:
            self.usuario = self.get_usuario(id_usuario)
        if rota and metodo:
            self.pesquisa = self.get_pesquisa(rota, metodo)
        if self.usuario and self.pesquisa:
            self.get_token()

    def get_usuario(self, identificacao):
        try:
            usuario = Usuario.objects.get(username=identificacao)
        except Usuario.DoesNotExist as error:
            raise ValidationError(message=error)

        return usuario

    def get_pesquisa(self, rota, metodo):
        try:
            pesquisa = Pesquisa.objects.get(
                (
                    (Q(periodo_inicio__isnull=True) &
                     Q(periodo_fim__isnull=True)) |
                    (Q(periodo_inicio__gte=datetime.datetime.now()) &
                     Q(periodo_fim__lte=datetime.datetime.now()))
                ),
                ativa=True,
                acao__sistema=self.usuario.sistema,
                acao__rota=rota,
                acao__metodo_requisicao=metodo
            )
        except Pesquisa.DoesNotExist as error:
            raise ValidationError(message=error)

        return pesquisa

    def get_token(self):
        token, created = Token.objects.get_or_create(usuario=self.usuario, pesquisa=self.pesquisa)

        if created or token.disponivel:
            token.gerar_token()
            self.url = self.get_url_pesquisa(token.token)
        else:
            self.url = None

    def get_url_pesquisa(self, token):
        return f'{settings.ADMIN_URL}/ces?token={token}'
