from ..views import SEGUNDO_PASSO, TERCEIRO_PASSO
from django.urls import reverse
import pytest

pytestmark = pytest.mark.django_db


def test_view_atribuir_nota_sem_passar_o_param_token(client):
    url = reverse('atribuir_nota')
    response = client.get(url)
    assert response.status_code == 200
    assert 'ces/pagina_invalida.html' in [t.name for t in response.templates]


def test_view_atribuir_nota(client, token_pesquisa_x):
    url = reverse('atribuir_nota') + f'?token={token_pesquisa_x.token}'
    response = client.get(url)

    assert response.status_code == 200
    assert 'ces/pesquisa_atribuir_nota.html' in [t.name for t in response.templates]

    data = {'nota': '5'}
    response = client.post(url, data)
    assert response.status_code == 302

    assert 'resposta_uuid' in client.session
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
    resposta_uuid = resposta_token_pesquisa_x.uuid
    session = client.session
    session['resposta_uuid'] = str(resposta_uuid)
    session.save()

    url = reverse('atribuir_comentario') + f'?token={token_pesquisa_x.token}'
    response = client.get(url)

    assert response.status_code == 200

    assert 'ces/pesquisa_atribuir_comentario.html' in [t.name for t in response.templates]

    data = {'comentario': 'Um bom comentário.'}
    response = client.post(url, data)
    assert response.status_code == 302

    redirect_url = reverse(TERCEIRO_PASSO)
    assert response.url == redirect_url
