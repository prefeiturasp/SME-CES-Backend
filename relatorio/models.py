import logging
from typing import Any
from django.db import models
from django.db.models import Sum
from django.core.files import File
from django.core.files.base import ContentFile
from django.dispatch import receiver
from django.db.models.signals import post_save
from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog

from comum.models import ModeloBase
from .services.relatorio_medias import gerar_csv

logger = logging.getLogger(__name__)


class Relatorio(ModeloBase):

    history = AuditlogHistoryField()

    coordenadoria = models.ForeignKey(
        'core.Coordenadoria', on_delete=models.PROTECT, blank=True, null=True)

    sistema = models.ForeignKey(
        'core.Sistema', on_delete=models.PROTECT, blank=True, null=True)

    pesquisa = models.ForeignKey(
        'pesquisa.Pesquisa', on_delete=models.PROTECT, blank=True, null=True)

    periodo_inicio = models.DateTimeField(
        verbose_name='Período início',
        blank=True, null=True
    )

    periodo_fim = models.DateTimeField(
        verbose_name='Período fim',
        blank=True, null=True
    )

    criado_por = models.ForeignKey(
        'usuario.Usuario', verbose_name='Criado por', on_delete=models.PROTECT, blank=True, null=True
    )

    arquivo = models.FileField('Arquivo', blank=True, null=True)

    class Meta:
        verbose_name = 'Relatório'
        verbose_name_plural = 'Relatórios'


@receiver(post_save, sender=Relatorio)
def gerar_relatorio(sender, instance, created, **kwargs):
    if created:
        gerar_csv(instance)


auditlog.register(Relatorio)
