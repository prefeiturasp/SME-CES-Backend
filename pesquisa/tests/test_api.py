import pytest
from rest_framework import status


pytestmark = pytest.mark.django_db


def test_buscar_pesquisa(
        token_authenticated_client,
        participante_sistema_xpto,
        payload_acao_xpto,
        pesquisa_x
):
    response = token_authenticated_client.get(
        f'/api/pesquisas/?identificacao_usuario={participante_sistema_xpto.username}&metodo_recurso_acao={payload_acao_xpto["metodo_requisicao"]}&recurso_acao={payload_acao_xpto["rota"]}', content_type='application/json')

    assert 'url' in response.json()
    assert response.json()['url'] != ''
    assert response.status_code == status.HTTP_200_OK


def test_buscar_pesquisa_nao_encontrada(
        token_authenticated_client,
        participante_sistema_xpto,
        payload_acao_zpto,
        pesquisa_x
):
    response = token_authenticated_client.get(
        f'/api/pesquisas/?identificacao_usuario={participante_sistema_xpto.username}&metodo_recurso_acao={payload_acao_zpto["metodo_requisicao"]}&recurso_acao={payload_acao_zpto["rota"]}', content_type='application/json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_buscar_pesquisa_inativa(
        token_authenticated_client,
        participante_sistema_xpto,
        pesquisa_y_inativa,
        payload_acao_xpto
):
    response = token_authenticated_client.get(
        f'/api/pesquisas/?identificacao_usuario={participante_sistema_xpto.username}&metodo_recurso_acao={payload_acao_xpto["metodo_requisicao"]}&recurso_acao={payload_acao_xpto["rota"]}', content_type='application/json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_validacao_buscar_pesquisa(
        token_authenticated_client,
        participante_sistema_xpto,
        payload_acao_zpto,
        pesquisa_x
):
    response = token_authenticated_client.get(
        f'/api/pesquisas/?metodo_recurso_acao={payload_acao_zpto["metodo_requisicao"]}&recurso_acao={payload_acao_zpto["rota"]}', content_type='application/json')

    expected_dict = {'erro': 'identificacao_usuario é obrigatório', 'mensagem': 'Parâmetros obrigatórios faltando.'}
    assert all(item in response.json().items() for item in expected_dict.items())
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_buscar_pesquisa_respondida(
        token_authenticated_client,
        participante_sistema_xpto,
        pesquisa_x,
        token_pesquisa_x,
        resposta_token_pesquisa_x,
        payload_acao_xpto
):
    response = token_authenticated_client.get(
        f'/api/pesquisas/?identificacao_usuario={participante_sistema_xpto.username}&metodo_recurso_acao={payload_acao_xpto["metodo_requisicao"]}&recurso_acao={payload_acao_xpto["rota"]}', content_type='application/json')

    assert response.data is None
    assert response.status_code == status.HTTP_200_OK
