import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog

from .constants import GRUPO_NIVEL_COORDENADORIA, GRUPO_NIVEL_PO
from .utils import envia_email_novo_usuario


class Usuario(AbstractUser):
    history = AuditlogHistoryField()
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, null=True)
    coordenadoria = models.ForeignKey(
        'core.Coordenadoria', on_delete=models.PROTECT, related_name="usuarios_coordenadoria", blank=True, null=True)
    sistema = models.ForeignKey(
        'core.Sistema', on_delete=models.PROTECT, related_name="usuarios_sistema", blank=True, null=True)

    def save(self, *args, **kwargs):
        self.email = self.username
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

    def enviar_email_redefinicao_senha(self):
        envia_email_novo_usuario(self)


@receiver(post_save, sender=Usuario)
def adiciona_grupo(sender, instance, created, **kwargs):
    if created:
        instance.enviar_email_redefinicao_senha()
        instance.is_staff = True
        instance.save()
    if instance.sistema is not None:
        instance.groups.add(Usuario.get_grupo_po())
    elif instance.coordenadoria is not None:
        instance.groups.add(Usuario.get_grupo_coordenadoria())


auditlog.register(Usuario)
