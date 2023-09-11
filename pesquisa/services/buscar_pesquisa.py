from django.core.exceptions import ValidationError
from django.conf import settings
from usuario.models import Usuario
from ..models import Pesquisa, Resposta
from .token_pesquisa import gerar_jwt_token, decodificar_jwt_token


def gerar_url_pesquisa(token):
    return f'{settings.DOMAIN_URL}/ces?token={token}'


def buscar_pesquisa(identificacao_usuario, rota, metodo_requisicao):
    try:
        usuario = Usuario.objects.get(username=identificacao_usuario)
    except Usuario.DoesNotExist as error:
        raise ValidationError(message=error)

    try:
        pesquisa = Pesquisa.objects.get(
            ativa=True,
            acao__rota=rota,
            acao__metodo_requisicao=metodo_requisicao
        )
    except Pesquisa.DoesNotExist as error:
        raise ValidationError(message=error)

    try:
        resposta = Resposta.objects.get(usuario=usuario, pesquisa=pesquisa)
    except Resposta.DoesNotExist:
        resposta = None

    if resposta is not None:
        if resposta.nota is not None:
            raise ValidationError(message='Pesquisa já foi respondida.')
        elif resposta.pulos >= pesquisa.limite_apos_pular:
            raise ValidationError(message='Limite de pulos excedido. Pesquisa não está mais disponível para o usuário solicitado.')

    return pesquisa, gerar_jwt_token(usuario.uuid, pesquisa.uuid)


def buscar_pesquisa_por_token(token):
    try:
        payload = decodificar_jwt_token(token)
    except Exception as error:
        raise ValidationError(message=error)

    try:
        usuario = Usuario.objects.get(uuid=payload['user_uuid'])
    except Usuario.DoesNotExist as error:
        raise ValidationError(message=error)

    try:
        pesquisa = Pesquisa.objects.get(uuid=payload['pesquisa_uuid'])
    except Pesquisa.DoesNotExist as error:
        raise ValidationError(message=error)

    try:
        resposta = Resposta.objects.get(usuario=usuario, pesquisa=pesquisa)
    except Resposta.DoesNotExist:
        resposta = None

    if resposta is not None:
        if resposta.nota is not None:
            raise ValidationError(message='Pesquisa já foi respondida.')
        elif resposta.pulos >= pesquisa.limite_apos_pular:
            raise ValidationError(message='Limite de pulos excedido. Pesquisa não está mais disponível para o usuário solicitado.')

    return pesquisa
