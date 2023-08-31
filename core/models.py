from django.db import models
from django.utils.text import slugify
from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog

from comum.models import ModeloIdNome


class Coordenadoria(ModeloIdNome):
    '''Classe que representa uma unidade administrativa'''

    codigo = models.CharField(
        "Codigo", max_length=255, null=False, blank=False)
    sigla = models.CharField("sigla", max_length=255, null=False, blank=False)

    def __str__(self):
        return '{} - {}'.format(self.codigo, self.sigla)

    class Meta:
        verbose_name = 'coordenadoria'
        verbose_name_plural = 'Coordenadorias'


class Sistema(ModeloIdNome):
    history = AuditlogHistoryField()

    coordenadoria = models.ForeignKey(
        'Coordenadoria', on_delete=models.PROTECT, related_name="sistemas", null=True)

    class Meta:
        verbose_name = "Sistema"
        verbose_name_plural = "Sistemas"


class Acao(ModeloIdNome):
    '''Classe que representa as acoes do sistema'''

    METODO_REQUISICAO_GET = 'GET'
    METODO_REQUISICAO_POST = 'POST'
    METODO_REQUISICAO_PUT = 'PUT'
    METODO_REQUISICAO_PATCH = 'PATCH'

    METODOS_REQUISICAO_NOMES = {
        METODO_REQUISICAO_GET: METODO_REQUISICAO_GET,
        METODO_REQUISICAO_POST: METODO_REQUISICAO_POST,
        METODO_REQUISICAO_PUT: METODO_REQUISICAO_PUT,
        METODO_REQUISICAO_PATCH: METODO_REQUISICAO_PATCH
    }

    METODOS_REQUISICAO_CHOICES = (
        (METODO_REQUISICAO_GET,
         METODOS_REQUISICAO_NOMES[METODO_REQUISICAO_GET]),
        (METODO_REQUISICAO_POST,
         METODOS_REQUISICAO_NOMES[METODO_REQUISICAO_POST]),
        (METODO_REQUISICAO_PUT,
         METODOS_REQUISICAO_NOMES[METODO_REQUISICAO_PUT]),
        (METODO_REQUISICAO_PATCH,
         METODOS_REQUISICAO_NOMES[METODO_REQUISICAO_PATCH])

    )
    history = AuditlogHistoryField()

    sistema = models.ForeignKey(
        'Sistema', on_delete=models.CASCADE, related_name="recursos", blank=True, null=True)
    modulo = models.CharField(
        "Modulo", max_length=255, blank=True, null=True)
    submodulo = models.CharField(
        "SubModulo", max_length=255, blank=True, null=True)

    rota = models.CharField('Rota', max_length=320)
    metodo_requisicao = models.CharField(
        'Método da requisição',
        max_length=15,
        choices=METODOS_REQUISICAO_CHOICES,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Ação do sistema"
        verbose_name_plural = "Ações do sistema"

    def save(self, *args, **kwargs):
        if self.modulo:
            self.modulo = slugify(self.modulo)

        if self.submodulo:
            self.submodulo = slugify(self.submodulo)

        super(Acao, self).save(*args, **kwargs)


auditlog.register(Sistema)
auditlog.register(Acao)
