
from django.contrib.auth.models import Group
from .constants import (GRUPO_NIVEL_API, GRUPO_NIVEL_COORDENADORIA,
                        GRUPO_NIVEL_PARTICIPANTE, GRUPO_NIVEL_SISTEMA)


class AuthService:
    @classmethod
    def get_sistema_group(cls):
        return Group.objects.get(name=GRUPO_NIVEL_SISTEMA)

    @classmethod
    def get_coordenadoria_group(cls):
        return Group.objects.get(name=GRUPO_NIVEL_COORDENADORIA)

    @classmethod
    def get_participante_group(cls):
        return Group.objects.get(name=GRUPO_NIVEL_PARTICIPANTE)

    @classmethod
    def get_api_group(cls):
        return Group.objects.get(name=GRUPO_NIVEL_API)
