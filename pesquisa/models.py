from django.db import models
from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog

from comum.models import ModeloIdNome


class Pesquisa(ModeloIdNome):
    '''Classe que representa uma pesquisa'''

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


auditlog.register(Pesquisa)
