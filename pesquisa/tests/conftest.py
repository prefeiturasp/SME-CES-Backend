import pytest
import datetime
from model_bakery import baker
from usuario.constants import GRUPO_NIVEL_COORDENADORIA, GRUPO_NIVEL_PO
from pesquisa.models import Token


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
def payload_token_nao_registrado():
    return 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c3VhcmlvIjoiMjlhZmRlNjgtZTZiYS00NTNjLWIyOWItZjIxMTUyMjRlM2I5IiwicGVzcXVpc2EiOiJjMzFhM2Q4OC0xYzI1LTRjOTctYTViMi1mZGQyNzBlMDIzYWUiLCJ0aW1lc3RhbXAiOjE2OTQ2NjA5NjMuOTQ4NTM1LCJleHAiOjE2OTQ2NTA3NjN9.scjtmkstXGpLwVqaReL3-bQXJj0aK-pV7ATZjU6B7kw'


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
def pesquisa_y_inativa(acao_xpto):
    return baker.make(
        'Pesquisa',
        acao=acao_xpto,
        ativa=False
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
    token = Token.objects.create(
        pesquisa=pesquisa_x,
        usuario=participante_sistema_xpto,
    )
    token.gerar_token()
    return token


@pytest.fixture
def token_pesquisa_y(pesquisa_y_inativa, participante_sistema_xpto):
    token = Token.objects.create(
        pesquisa=pesquisa_y_inativa,
        usuario=participante_sistema_xpto,
    )
    token.gerar_token()
    return token


@pytest.fixture
def token_pesquisa_x_expirado(pesquisa_x, participante_sistema_xpto):
    token = Token.objects.create(
        pesquisa=pesquisa_x,
        usuario=participante_sistema_xpto,
    )
    expiracao = datetime.datetime.utcnow() - datetime.timedelta(minutes=10)
    token.gerar_token(expiracao)
    return token


@pytest.fixture
def resposta_token_pesquisa_x(token_pesquisa_x):
    return baker.make(
        'Resposta',
        token=token_pesquisa_x,
        nota=5,
    )


@pytest.fixture
def resposta_token_pesquisa_y(token_pesquisa_y):
    return baker.make(
        'Resposta',
        token=token_pesquisa_y,
        nota=5,
    )
