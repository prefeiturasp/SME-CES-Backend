import logging
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema
from pesquisa.models import Token
from .services.pesquisa import BuscarPesquisaService
from usuario.permissions import IsAPIUser

logger = logging.getLogger(__name__)

PRIMEIRO_PASSO = 'atribuir_nota'
SEGUNDO_PASSO = 'atribuir_comentario'
TERCEIRO_PASSO = 'agradecimento'


def handle_validation(request, step=None):
    """
    Função utilitária para lidar com a recuperação e validação do token.
    Retorna a instância do token se for válida, ou None e uma mensagem de erro ao usuário se não for.
    """
    token = request.GET.get('token')

    if token:
        request.session["token"] = token
    else:
        token = request.session.get("token")

    if not token:
        return None, 'Token requerido.'

    try:
        token_instance = Token.objects.get(token=token)
    except Token.DoesNotExist:
        return None, 'Token não encontrado.'

    if not token_instance.token_valido:
        return None, 'Token inválido.'

    if not token_instance.pesquisa.valida:
        return None, 'A pesquisa não está mais disponível.'

    if step == 1:
        if token_instance.respondida:
            return None, 'A pesquisa já foi respondida.'

    if step == 2:
        if not token_instance.respondida:
            return None, 'Operação inválida.'

    return token_instance, None


def atribuir_nota_view(request):
    token, erro = handle_validation(request, step=1)
    if token:
        if request.method == 'POST':
            try:
                nota = request.POST['nota']
            except Exception:
                nota = None

            if nota:
                token.atribuir_resposta(nota)
                return redirect(reverse(SEGUNDO_PASSO))
            else:
                del request.session['token']
                token.responder_depois()
                return redirect(reverse(TERCEIRO_PASSO))
        else:
            return render(request, 'ces/pesquisa_atribuir_nota.html', {'afirmacao': token.pesquisa.afirmacao})
    else:
        return render(request, 'ces/pagina_invalida.html', {'mensagem': erro})


def atribuir_comentario_view(request):
    token, erro = handle_validation(request, step=2)

    if token:
        if request.method == 'POST':
            try:
                comentario = request.POST['comentario']
            except Exception as err:
                comentario = None

            if comentario:
                token.atribuir_comentario(comentario)

            del request.session['token']
            return redirect(reverse(TERCEIRO_PASSO))
        else:
            return render(request, 'ces/pesquisa_atribuir_comentario.html')
    else:
        return render(request, 'ces/pagina_invalida.html', {'mensagem': erro})


def agradecimento_view(request):
    return render(request, 'ces/pesquisa_agradecimento.html')


@extend_schema(
    parameters=[
        OpenApiParameter(name='identificacao_usuario', description='Identificação do usuário(rf, email)', required=True, type=OpenApiTypes.STR),
        OpenApiParameter(name='recurso_acao', description='Rota da api', required=True, type=OpenApiTypes.STR),
        OpenApiParameter(name='metodo_recurso_acao', description='Método da rota da api', required=True, type=OpenApiTypes.STR),
    ],
    description='Busca pesquisa disponível para o recurso e usuário especificado.'
)
class PesquisasView(APIView):
    permission_classes = [IsAuthenticated & IsAPIUser]
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        identificacao_usuario = request.query_params.get('identificacao_usuario')
        recurso_acao = request.query_params.get('recurso_acao')
        metodo_recurso_acao = request.query_params.get('metodo_recurso_acao')

        if identificacao_usuario is None:
            return Response({"erro": "identificacao_usuario é obrigatório", "mensagem": "Parâmetros obrigatórios faltando."},
                            status=status.HTTP_400_BAD_REQUEST)
        if recurso_acao is None or metodo_recurso_acao is None:
            return Response({"erro": "'recurso_acao' é obrigatório, 'metodo_recurso_acao' é obrigatório", "mensagem": "Parâmetros obrigatórios faltando."},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            service = BuscarPesquisaService(identificacao_usuario, recurso_acao, metodo_recurso_acao)
        except Exception as error:
            logger.error('Erro buscar pesquisa: %r', error)
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

        if service.url:
            resp = {'url': service.url}
        else:
            resp = None

        return Response(resp, status=status.HTTP_200_OK)
