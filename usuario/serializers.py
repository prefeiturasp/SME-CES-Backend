from rest_framework import serializers
from .models import Usuario


class CadastroUsuarioSerializer(serializers.Serializer):
    identificacao = serializers.CharField()
