from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .services.buscar_pesquisa import buscar_pesquisa, buscar_pesquisa_por_token, gerar_url_pesquisa
from drf_spectacular.utils import extend_schema, extend_schema_view
from drf_spectacular.utils import OpenApiExample, OpenApiResponse, OpenApiParameter, OpenApiTypes
# window.open("http://localhost:8000/pesquisa/ces/comentario", "_blank", "toolbar=no, location=no, directories=no,status=no, menubar=no, scrollbars=yes, resizable=yes, copyhistory=yes, width=600, height=600");


def pesquisa_passo_um(request):
    token = request.GET.get('token')

    try:
        pesquisa = buscar_pesquisa_por_token(token)
        return render(request, 'ces/pesquisa_passo_um.html', {'afirmacao': pesquisa.afirmacao})
    except Exception as error:
        # print(error)
        return render(request, 'ces/pagina_invalida.html')


def pesquisa_passo_dois(request):
    return render(request, 'ces/pesquisa_passo_dois.html')


def pesquisa_passo_tres(request):
    return render(request, 'ces/pesquisa_passo_tres.html')


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
            pesquisa, token = buscar_pesquisa(
                identificacao_usuario,
                recurso_acao,
                metodo_recurso_acao
            )
        except Exception as e:
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)

        url = gerar_url_pesquisa(token)

        return Response({'url': url}, status=status.HTTP_200_OK)
