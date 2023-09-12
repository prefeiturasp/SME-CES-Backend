import logging
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema

from .services.pesquisa import PesquisaService
# window.open("http://localhost:8000/pesquisa/ces/comentario", "_blank", "toolbar=no, location=no, directories=no,status=no, menubar=no, scrollbars=yes, resizable=yes, copyhistory=yes, width=600, height=600");
logger = logging.getLogger(__name__)

PRIMEIRO_PASSO = 'atribuir_nota'
SEGUNDO_PASSO = 'atribuir_comentario'
TERCEIRO_PASSO = 'agradecimento'


def handle_token(request):
    """
    Função utilitária para lidar com a recuperação e validação de tokens.
    Retorna a instância do token se for válida, ou None se não for.
    """
    token = request.GET.get('token')

    if token:
        request.session["token"] = token
    else:
        token = request.session.get("token")

    try:
        service = PesquisaService(token=token)

        if not service.token_instance:
            raise ValidationError(message='Token requerido')

        return service.token_instance
    except Exception as err:
        print(err)
        return None


def atribuir_nota_view(request):
    token_instance = handle_token(request)

    if token_instance and token_instance.disponivel:
        if request.method == 'POST':
            try:
                nota = request.POST['nota']
            except Exception:
                nota = None

            if nota:
                resposta = token_instance.atribuir_resposta(nota)
                request.session["resposta_uuid"] = str(resposta.uuid)
                return redirect(reverse(SEGUNDO_PASSO))
            else:
                del request.session['token']
                token_instance.responder_depois()
                return redirect(reverse(TERCEIRO_PASSO))
        else:
            return render(request, 'ces/pesquisa_atribuir_nota.html', {'afirmacao': token_instance.pesquisa.afirmacao})
    else:
        return render(request, 'ces/pagina_invalida.html')


def atribuir_comentario_view(request):
    token = handle_token(request)

    if not token:
        return render(request, 'ces/pagina_invalida.html')
    try:
        resposta_uuid = request.session.get("resposta_uuid")
    except Exception as err:
        logger.error(err)
        return render(request, 'ces/pagina_invalida.html')

    try:
        resposta = token.respostas.get(uuid=resposta_uuid)
        if resposta.comentario:
            raise ValidationError(message='Pesquisa indisponível')
    except Exception as err:
        logger.error(err)
        return render(request, 'ces/pagina_invalida.html')

    if request.method == 'POST':
        try:
            comentario = request.POST['comentario']
        except Exception as err:
            logger.error(err)
            comentario = None

        if comentario:
            token.atribuir_comentario(resposta_uuid, comentario)

        del request.session['token']
        del request.session['resposta_uuid']
        return redirect(reverse(TERCEIRO_PASSO))
    else:
        return render(request, 'ces/pesquisa_atribuir_comentario.html')


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
    permission_classes = [IsAuthenticated]
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
            service = PesquisaService(identificacao_usuario, recurso_acao, metodo_recurso_acao)
            url = service.get_token_pesquisa()
        except Exception as e:
            print(e)
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'url': url}, status=status.HTTP_200_OK)
