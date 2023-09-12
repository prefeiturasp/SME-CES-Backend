import pytest
from model_bakery import baker
from usuario.constants import GRUPO_NIVEL_COORDENADORIA, GRUPO_NIVEL_PO


@pytest.fixture
def grupo_coordenadoria():
    return baker.make(
        'Group',
        name=GRUPO_NIVEL_COORDENADORIA
    )


@pytest.fixture
def grupo_po():
    return baker.make(
        'Group',
        name=GRUPO_NIVEL_PO
    )


@pytest.fixture
def sistema_xpto():
    return baker.make(
        'Sistema',
        nome='Sistame XPTO'
    )


@pytest.fixture
def usuario_sistema_xpto(sistema_xpto, grupo_po):
    return baker.make(
        'Usuario',
        username='sistema_xpto',
        first_name='sistema_xpto',
        sistema=sistema_xpto
    )


@pytest.fixture
def token_authenticated_client(usuario_sistema_xpto):
    from rest_framework.test import APIClient
    api_client = APIClient()
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {usuario_sistema_xpto.auth_token}')
    return api_client


@pytest.fixture
def payload_acao_xpto():
    return {
        'rota': '/api/despesa/',
        'metodo_requisicao': 'POST'
    }


@pytest.fixture
def payload_acao_zpto():
    return {
        'rota': '/api/receita/',
        'metodo_requisicao': 'POST'
    }


@pytest.fixture
def acao_xpto(sistema_xpto):
    return baker.make(
        'Acao',
        nome='Criar nova despesa',
        sistema=sistema_xpto,
        rota='/api/despesa/',
        metodo_requisicao='POST'
    )


@pytest.fixture
def pesquisa_x(acao_xpto):
    return baker.make(
        'Pesquisa',
        acao=acao_xpto
    )


@pytest.fixture
def participante_sistema_xpto(sistema_xpto, grupo_po):
    return baker.make(
        'Usuario',
        username='Participante 1 sistema XPTO',
        first_name='sistema_xpto',
        sistema=sistema_xpto
    )


@pytest.fixture
def token_pesquisa_x(pesquisa_x, participante_sistema_xpto):
    return baker.make(
        'pesquisa.Token',
        pesquisa=pesquisa_x,
        usuario=participante_sistema_xpto,
    )


@pytest.fixture
def resposta_token_pesquisa_x(token_pesquisa_x):
    return baker.make(
        'Resposta',
        token=token_pesquisa_x,
        nota=5,
    )
