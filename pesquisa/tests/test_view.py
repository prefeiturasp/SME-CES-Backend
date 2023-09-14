from ..views import SEGUNDO_PASSO, TERCEIRO_PASSO
from django.urls import reverse
import pytest

pytestmark = pytest.mark.django_db


def test_validacao_token_requerido_view_atribuir_nota(client):
    url = reverse('atribuir_nota')
    response = client.get(url)
    assert response.status_code == 200
    assert 'Token requerido.' in response.content.decode()
    assert 'ces/pagina_invalida.html' in [t.name for t in response.templates]

    url = reverse('atribuir_comentario')
    response = client.get(url)
    assert response.status_code == 200
    assert 'Token requerido.' in response.content.decode()
    assert 'ces/pagina_invalida.html' in [t.name for t in response.templates]


def test_validacao_token_nao_encontrado_view_atribuir_nota(client, payload_token_nao_registrado):
    url = reverse('atribuir_nota') + f'?token={payload_token_nao_registrado}'
    response = client.get(url)
    assert response.status_code == 200
    assert 'Token não encontrado.' in response.content.decode()
    assert 'ces/pagina_invalida.html' in [t.name for t in response.templates]

    url = reverse('atribuir_comentario') + f'?token={payload_token_nao_registrado}'
    response = client.get(url)
    assert response.status_code == 200
    assert 'Token não encontrado.' in response.content.decode()
    assert 'ces/pagina_invalida.html' in [t.name for t in response.templates]


def test_validacao_token_invalido_view_atribuir_nota(client, token_pesquisa_x_expirado):
    url = reverse('atribuir_nota') + f'?token={token_pesquisa_x_expirado.token}'
    response = client.get(url)
    assert response.status_code == 200
    assert 'Token inválido.' in response.content.decode()
    assert 'ces/pagina_invalida.html' in [t.name for t in response.templates]

    url = reverse('atribuir_comentario') + f'?token={token_pesquisa_x_expirado.token}'
    response = client.get(url)
    assert response.status_code == 200
    assert 'Token inválido.' in response.content.decode()
    assert 'ces/pagina_invalida.html' in [t.name for t in response.templates]


def test_validacao_pesquisa_inativa_view_atribuir_nota(client, pesquisa_y_inativa, token_pesquisa_y):
    url = reverse('atribuir_nota') + f'?token={token_pesquisa_y.token}'
    response = client.get(url)
    assert response.status_code == 200
    assert 'A pesquisa não está mais disponível.' in response.content.decode()
    assert 'ces/pagina_invalida.html' in [t.name for t in response.templates]

    url = reverse('atribuir_comentario') + f'?token={token_pesquisa_y.token}'
    response = client.get(url)
    assert response.status_code == 200
    assert 'A pesquisa não está mais disponível.' in response.content.decode()
    assert 'ces/pagina_invalida.html' in [t.name for t in response.templates]


def test_validacao_pesquisa_respondida_view_atribuir_nota(client, pesquisa_x, token_pesquisa_x, resposta_token_pesquisa_x):
    url = reverse('atribuir_nota') + f'?token={token_pesquisa_x.token}'
    response = client.get(url)
    assert response.status_code == 200
    assert 'A pesquisa já foi respondida.' in response.content.decode()
    assert 'ces/pagina_invalida.html' in [t.name for t in response.templates]


def test_validacao_pesquisa_nao_respondida_view_atribuir_comentario(client, pesquisa_x, token_pesquisa_x):
    url = reverse('atribuir_comentario') + f'?token={token_pesquisa_x.token}'
    response = client.get(url)
    assert response.status_code == 200
    assert 'Operação inválida.' in response.content.decode()
    assert 'ces/pagina_invalida.html' in [t.name for t in response.templates]


def test_view_atribuir_nota(client, token_pesquisa_x):

    url = reverse('atribuir_nota') + f'?token={token_pesquisa_x.token}'
    response = client.get(url)

    assert response.status_code == 200
    assert 'ces/pesquisa_atribuir_nota.html' in [t.name for t in response.templates]

    data = {'nota': '5'}
    response = client.post(url, data)
    assert response.status_code == 302

    assert 'token' in client.session

    redirect_url = reverse(SEGUNDO_PASSO)
    assert response.url == redirect_url


def test_view_atribuir_nota_pular_resposta(client, token_pesquisa_x):
    url = reverse('atribuir_nota') + f'?token={token_pesquisa_x.token}'
    response = client.get(url)

    assert response.status_code == 200
    assert 'ces/pesquisa_atribuir_nota.html' in [t.name for t in response.templates]

    response = client.post(url)
    assert response.status_code == 302

    redirect_url = reverse(TERCEIRO_PASSO)
    assert response.url == redirect_url


def test_view_atribuir_comentario(client, token_pesquisa_x, resposta_token_pesquisa_x):

    url = reverse('atribuir_comentario') + f'?token={token_pesquisa_x.token}'
    response = client.get(url)

    assert response.status_code == 200

    assert 'ces/pesquisa_atribuir_comentario.html' in [t.name for t in response.templates]

    data = {'comentario': 'Um bom comentário.'}
    response = client.post(url, data)
    assert response.status_code == 302

    redirect_url = reverse(TERCEIRO_PASSO)
    assert response.url == redirect_url
