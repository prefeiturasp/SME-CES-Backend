from django.db import models
from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog

from comum.models import ModeloBase


class Pesquisa(ModeloBase):

    history = AuditlogHistoryField()

    acao = models.ForeignKey(
        'core.Acao', on_delete=models.PROTECT, related_name="pesquisas", blank=True, null=True)

    ativa = models.BooleanField('Ativa?', default=True)
    periodo_inicio = models.DateTimeField('Período início', help_text='A pesquisa só estará ativa a partir dessa data.', blank=True, null=True)
    periodo_fim = models.DateTimeField('Período fim', help_text='A pesquisa só estará ativa até essa data', blank=True, null=True)
    limite_apos_pular = models.PositiveIntegerField(
        'Limite após pular', help_text='Quantidade de vezes que a pesquisa continuará sendo retornada, mesmo que o usuário pule.', default=0)
    afirmacao = models.TextField('Afirmação', default='Consegui o resultado esperado com a ação que acabei de realizar?')

    class Meta:
        verbose_name = 'Pesquisa'
        verbose_name_plural = 'Pesquisas'


class Resposta(ModeloBase):

    history = AuditlogHistoryField()

    pesquisa = models.ForeignKey(
        'Pesquisa', on_delete=models.PROTECT, related_name="respostas", blank=True, null=True)
    usuario = models.ForeignKey(
        'usuario.Usuario', on_delete=models.PROTECT, blank=True, null=True
    )
    nota = models.PositiveIntegerField('Nota', blank=True, null=True)
    quantidade_pulos = models.PositiveIntegerField('Quantidade de pulos', help_text='Quantidade de vezes em que o usuário pulou a pesquisa.', default=0)

    class Meta:
        verbose_name = 'Resposta'
        verbose_name_plural = 'Respostas'


auditlog.register(Pesquisa)
auditlog.register(Resposta)
