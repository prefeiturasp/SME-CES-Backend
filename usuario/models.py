import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.dispatch import receiver
from django.db.models.signals import post_save

from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog

from .constants import GRUPO_NIVEL_COORDENADORIA, GRUPO_NIVEL_PO


class Usuario(AbstractUser):
    history = AuditlogHistoryField()
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, null=True)
    coordenadoria = models.ForeignKey(
        'core.Coordenadoria', on_delete=models.PROTECT, related_name="usuarios_coordenadoria", blank=True, null=True)
    sistema = models.ForeignKey(
        'core.Sistema', on_delete=models.PROTECT, related_name="usuarios_sistema", blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.sistema:
            self.coordenadoria = self.sistema.coordenadoria
        super(Usuario, self).save(*args, **kwargs)

    @property
    def is_coordenador(self):
        return self.groups.filter(name=GRUPO_NIVEL_COORDENADORIA).exists()

    @property
    def is_po(self):
        return self.groups.filter(name=GRUPO_NIVEL_PO).exists()

    @staticmethod
    def get_grupo_coordenadoria():
        return Group.objects.get(name=GRUPO_NIVEL_COORDENADORIA)

    @staticmethod
    def get_grupo_po():
        return Group.objects.get(name=GRUPO_NIVEL_PO)


@receiver(post_save, sender=Usuario)
def adiciona_grupo(sender, instance, created, **kwargs):
    if created and instance.sistema is not None:
        instance.groups.add(Usuario.get_grupo_po())
    elif created and instance.coordenadoria is not None:
        instance.groups.add(Usuario.get_grupo_coordenadoria())


auditlog.register(Usuario)
