import logging
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from .models import Usuario
from .serializers import CadastroUsuarioSerializer
from .permissions import IsAPIUser

logger = logging.getLogger(__name__)


class UsuariosView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated & IsAPIUser]
    serializer_class = CadastroUsuarioSerializer
    queryset = Usuario.objects.all()
    http_method_names = ['post']

    @extend_schema(
        request=CadastroUsuarioSerializer,
        responses={201: {}},
        description='Cadastra usuário participante.'
    )
    def create(self, request, *args, **kwargs):
        sistema_usuario = request.user.sistema
        identificacao = request.data.get('identificacao', None)
        try:
            usuario = Usuario.objects.create(username=identificacao,
                                             sistema=sistema_usuario)
            usuario.set_usuario_participante()
            return Response(status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'erro': 'Usuário já existe.'}, status=status.HTTP_400_BAD_REQUEST)
