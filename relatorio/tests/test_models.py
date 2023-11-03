import pytest
from django.utils import timezone
from datetime import timedelta
from core.models import Coordenadoria, Sistema, Acao
from pesquisa.models import Pesquisa, Resposta
from ..models import Relatorio
from usuario.models import Usuario
from ..services.relatorio_medias import get_infos, gerar_csv


@pytest.fixture
def relatorio_fixture(db):
    coordenadoria = Coordenadoria.objects.create(nome='Coordenadoria de Teste')
    sistema = Sistema.objects.create(nome='Sistema de Teste', coordenadoria=coordenadoria)
    pesquisa = Pesquisa.objects.create(acao=Acao.objects.create(nome='Ação de Teste', sistema=sistema))
    relatorio = Relatorio.objects.create(
        coordenadoria=coordenadoria,
        sistema=sistema,
        pesquisa=pesquisa,
        periodo_inicio=timezone.now() - timedelta(days=30),
        periodo_fim=timezone.now() + timedelta(days=30),
        criado_por=Usuario.objects.create(username='testuser')
    )
    yield relatorio


@pytest.fixture
def participante_fixture(db):
    yield Usuario.objects.create(username='participante')


@pytest.fixture
def participante_2_fixture(db):
    yield Usuario.objects.create(username='participante_2')


def test_get_infos(relatorio_fixture):
    relatorio = relatorio_fixture
    media, qnt_respostas, qnt_pulos = get_infos(relatorio, relatorio.pesquisa)

    assert media == 0
    assert qnt_respostas == 0
    assert qnt_pulos == 0


def test_get_infos_com_respostas(relatorio_fixture, participante_fixture, participante_2_fixture):
    relatorio = relatorio_fixture

    pesquisa = relatorio.pesquisa
    Resposta.objects.create(token=pesquisa.tokens.create(usuario=participante_fixture), nota=1, criado_em=timezone.now())
    Resposta.objects.create(token=pesquisa.tokens.create(usuario=participante_2_fixture), nota=2, criado_em=timezone.now())

    media, qnt_respostas, qnt_pulos = get_infos(relatorio, pesquisa)

    assert media == 1.5
    assert qnt_respostas == 2
    assert qnt_pulos == 0


def test_gerar_csv(relatorio_fixture):
    relatorio = relatorio_fixture
    gerar_csv(relatorio)

    assert relatorio.arquivo.name.endswith('.csv')
