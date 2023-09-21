import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, UserManager
from django.dispatch import receiver
from django.db.models.signals import post_save

from rest_framework.authtoken.models import Token

from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog

from .constants import GRUPO_NIVEL_COORDENADORIA, GRUPO_NIVEL_SISTEMA
from .utils import envia_email_novo_usuario
from .services import AuthService


class UsuariosParticipantes(models.Manager):
    def get_queryset(self):
        return super(UsuariosParticipantes, self).get_queryset().filter(groups=AuthService.get_participante_group())


class Usuario(AbstractUser):
    history = AuditlogHistoryField()
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, null=True)
    nome = models.CharField(verbose_name='Nome', max_length=250, blank=True)
    coordenadoria = models.ForeignKey(
        'core.Coordenadoria', on_delete=models.PROTECT, related_name="usuarios_coordenadoria", blank=True, null=True)
    sistema = models.ForeignKey(
        'core.Sistema', on_delete=models.PROTECT, related_name="usuarios_sistema", blank=True, null=True)

    objects = UserManager()

    participantes = UsuariosParticipantes()

    def save(self, *args, **kwargs):
        if self.sistema:
            self.coordenadoria = self.sistema.coordenadoria
        super(Usuario, self).save(*args, **kwargs)

    @property
    def is_coordenador(self):
        return self.groups.filter(name=GRUPO_NIVEL_COORDENADORIA).exists()

    @property
    def is_po(self):
        return self.groups.filter(name=GRUPO_NIVEL_SISTEMA).exists()

    def set_usuario_participante(self):
        self.groups.add(AuthService.get_participante_group())

    def set_usuario_coordenador(self):
        self.groups.add(AuthService.get_coordenadoria_group())

    def set_usuario_sistema(self):
        self.groups.add(AuthService.get_sistema_group())

    def set_usuario_api(self):
        self.groups.add(AuthService.get_api_group())
        self.atribui_token()

    @staticmethod
    def get_grupo_coordenadoria():
        return Group.objects.get(name=GRUPO_NIVEL_COORDENADORIA)

    @staticmethod
    def get_grupo_po():
        return Group.objects.get(name=GRUPO_NIVEL_SISTEMA)

    def enviar_email_redefinicao_senha(self):
        envia_email_novo_usuario(self)

    def atribui_token(self):
        Token.objects.get_or_create(user=self)


@receiver(post_save, sender=Usuario)
def apos_criar_usuario(sender, instance, created, **kwargs):
    if instance.sistema is not None:
        instance.set_usuario_sistema()
    elif instance.coordenadoria is not None:
        instance.set_usuario_coordenador()
    if created:
        if instance.is_staff and instance.email:
            instance.enviar_email_redefinicao_senha()


auditlog.register(Usuario)
