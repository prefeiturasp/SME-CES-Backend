import jwt
import datetime
from django.db import models
from django.conf import settings
from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog

from comum.models import ModeloBase


class Pesquisa(ModeloBase):

    history = AuditlogHistoryField()

    acao = models.ForeignKey(
        'core.Acao', on_delete=models.PROTECT, related_name="pesquisas", blank=True, null=True)

    ativa = models.BooleanField('Ativa?', default=True)

    anonima = models.BooleanField(
        verbose_name='Respostas Anônimas',
        help_text='Marque esta opção se deseja que as respostas sejam anônimas e não tenham relação direta com o participante.',
        default=False
    )

    periodo_inicio = models.DateTimeField(
        verbose_name='Período início',
        help_text='A pesquisa só estará ativa a partir dessa data.',
        blank=True, null=True
    )

    periodo_fim = models.DateTimeField(
        verbose_name='Período fim',
        help_text='A pesquisa só estará ativa até essa data',
        blank=True, null=True
    )

    limite_pular = models.PositiveIntegerField(
        verbose_name='Limite de Pulos na Pesquisa',
        help_text='Quantidade máxima de vezes que um usuário pode pular a pesquisa antes de não ser mais apresentada.',
        default=0
    )

    afirmacao = models.TextField(
        verbose_name='Afirmação da Pesquisa',
        help_text='A afirmação que a pesquisa apresenta aos participantes para avaliação.',
        default='Consegui o resultado esperado com a ação que acabei de realizar?'
    )

    validade_token = models.IntegerField(
        verbose_name='Tempo de Validade do Token (em minutos)',
        help_text='O período de tempo, em minutos, durante o qual o token de pesquisa permanece válido. Se o usuário não responder dentro desse período, a pesquisa ficará indisponível até que seja gerado um novo token.',
        default=10
    )

    def __str__(self):
        return self.acao.nome + ' | ' + self.acao.sistema.nome

    @property
    def periodo_valido(self):
        now = datetime.datetime.now()

        if self.periodo_inicio is None and self.periodo_fim is None:
            return True
        if self.periodo_inicio >= now and self.periodo_fim <= now:
            return True
        return False

    @property
    def valida(self):
        return self.ativa and self.periodo_valido

    class Meta:
        verbose_name = 'Pesquisa'
        verbose_name_plural = 'Pesquisas'


class Token(ModeloBase):

    history = AuditlogHistoryField()

    pesquisa = models.ForeignKey(
        'Pesquisa', on_delete=models.PROTECT, related_name="tokens", blank=False, null=False)
    usuario = models.ForeignKey(
        'usuario.Usuario', on_delete=models.PROTECT, blank=True, null=True
    )
    token = models.TextField('Token', blank=True, null=True)

    pulos = models.PositiveIntegerField('Pulos', help_text='Quantidade de vezes em que o usuário pulou a pesquisa.', default=0)

    class Meta:
        verbose_name = 'Token'
        verbose_name_plural = 'Tokens'

    def save(self, *args, **kwargs):
        if not self.token:
            self.gerar_token()

        return super().save(*args, **kwargs)

    @property
    def respondida(self):
        return self.respostas.exists()

    @property
    def disponivel(self):
        return self.pesquisa.valida and not self.respondida and not self.pulos_excedidos

    @property
    def pulos_excedido(self):
        return self.pulos > 0 and (self.pulos >= self.pesquisa.limite_pular)

    def gerar_token(self):
        expiracao = datetime.datetime.utcnow() + datetime.timedelta(minutes=self.pesquisa.validade_token)
        payload = {
            'usuario': str(self.usuario.uuid),
            'pesquisa': str(self.pesquisa.uuid),
            'exp': expiracao,
        }
        self.token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    def token_valido(self):
        try:
            payload = jwt.decode(self.token, settings.SECRET_KEY, algorithms=['HS256'])
            payload['usuario']
            payload['pesquisa']
        except jwt.ExpiredSignatureError:
            return False
        except jwt.DecodeError:
            return False
        except Exception:
            return False
        return True

    def responder_depois(self):
        self.pulos += 1
        self.save()

    def atribuir_resposta(self, nota):
        resposta = self.respostas.create(nota=nota)
        return resposta

    def atribuir_comentario(self, resposta_uuid, comentario):
        resposta = self.respostas.get(uuid=resposta_uuid)
        resposta.comentario = comentario
        resposta.save()


class Resposta(ModeloBase):

    history = AuditlogHistoryField()

    token = models.ForeignKey('Token', on_delete=models.PROTECT,
                              related_name="respostas",
                              blank=True, null=True)
    nota = models.PositiveIntegerField('Nota', blank=False, null=False, default=0)
    comentario = models.TextField('Comentário', blank=True, null=True)

    class Meta:
        verbose_name = 'Resposta'
        verbose_name_plural = 'Respostas'


auditlog.register(Pesquisa)
auditlog.register(Resposta)
