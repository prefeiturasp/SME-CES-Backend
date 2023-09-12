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
