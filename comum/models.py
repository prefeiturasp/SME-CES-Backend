import uuid as uuid

from django.db import models


class Descritivel(models.Model):
    descricao = models.TextField('Descrição', blank=True, null=True)

    class Meta:
        abstract = True


class TemNome(models.Model):
    nome = models.CharField('Nome', max_length=160)

    class Meta:
        abstract = True


class TemAtivo(models.Model):
    ativo = models.BooleanField("Está ativo?", default=True)

    class Meta:
        abstract = True


class TemCriadoEm(models.Model):
    criado_em = models.DateTimeField(
        "Criado em", editable=False, auto_now_add=True)

    class Meta:
        abstract = True


class TemAlteradoEm(models.Model):
    alterado_em = models.DateTimeField(
        "Alterado em", editable=False, auto_now=True)

    class Meta:
        abstract = True


class TemChaveExterna(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    @classmethod
    def by_uuid(cls, uuid):
        return cls.objects.get(uuid=uuid)

    class Meta:
        abstract = True


class ModeloBase(TemChaveExterna, TemCriadoEm, TemAlteradoEm):
    # Expoe explicitamente o model manager para evitar falsos alertas de Unresolved attribute reference for class Model
    objects = models.Manager()

    @classmethod
    def get_valores(cls, user=None, associacao_uuid=None):
        return cls.objects.all()

    @classmethod
    def by_id(cls, id):
        return cls.objects.get(id=id)

    class Meta:
        abstract = True


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Impede a exclusão do Singleton. A não ser que esse método seja sobreposto.
        pass

    @classmethod
    def get(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class ModeloIdNome(ModeloBase, TemNome):

    @classmethod
    def get_valores(cls, user=None, associacao_uuid=None):
        return cls.objects.all().order_by('nome')

    def __str__(self):
        return f"{self.nome}"

    class Meta:
        abstract = True
