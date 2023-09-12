import datetime
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db.models import Q
from usuario.models import Usuario
from ..models import Pesquisa, Token


class PesquisaService:
    def __init__(self, id_usuario=None, rota=None, metodo=None, token=None):
        print(id_usuario)
        if id_usuario:
            self.usuario = self.get_usuario(id_usuario)
        if rota and metodo:
            self.pesquisa = self.get_pesquisa(rota, metodo)
        if token:
            self.token_instance = self.get_token_by_key(token)
        else:
            self.token_instance = None

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
                     Q(periodo_inicio__lte=datetime.datetime.now()))
                ),
                ativa=True,
                acao__sistema=self.usuario.sistema,
                acao__rota=rota,
                acao__metodo_requisicao=metodo
            )
        except Pesquisa.DoesNotExist as error:
            raise ValidationError(message=error)

        return pesquisa

    def get_token_by_key(self, token):
        try:
            token_instance = Token.objects.get(token=token)
        except Token.DoesNotExist as error:
            raise ValidationError(message=error)

        return token_instance

    def get_token_pesquisa(self):
        token, created = Token.objects.get_or_create(usuario=self.usuario, pesquisa=self.pesquisa)

        if created or token.disponivel:
            if token.token_valido():
                return self.get_url_pesquisa(token.token)
            else:
                token.gerar_token()
                token.save()
                return self.get_url_pesquisa(token.token)

        return None

    def get_url_pesquisa(self, token):
        return f'{settings.DOMAIN_URL}/ces?token={token}'
