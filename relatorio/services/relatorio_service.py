import logging
import csv
from django.db.models import Sum
from tempfile import NamedTemporaryFile
from pesquisa.models import Pesquisa
from usuario.models import Usuario
logger = logging.getLogger(__name__)

def get_infos(relatorio, pesquisa):
    media = 0
    qnt_respostas = 0
    qnt_pulos = 0

    tokens_com_resposta = pesquisa.tokens.filter(resposta__isnull=False,
                                                 resposta__criado_em__gte=relatorio.periodo_inicio,
                                                 resposta__criado_em__lte=relatorio.periodo_fim)

    total_ocorrencias = 0
    for peso in [1, 2, 3, 4, 5, 6, 7]:
        total_ocorrencias += tokens_com_resposta.filter(resposta__nota=peso).count() * peso

    try:
        media = round(total_ocorrencias/tokens_com_resposta.count(), 2)
    except Exception as error:
        logger.error('get_infos: %r', error)
        media = 0

    qnt_respostas = tokens_com_resposta.count()

    if pesquisa.tokens.exists():
        qnt_pulos = pesquisa.tokens.aggregate(total=Sum('pulos'))['total']

    return media, qnt_respostas, qnt_pulos


def gerar_csv(relatorio):
    with NamedTemporaryFile(mode="r+", prefix='relatorio', suffix='.csv') as tmp:
        escritor_csv = csv.writer(tmp.file, delimiter=";")

        escritor_csv.writerow(['coordenadoria', 'sistema', 'pesquisa', 'media', 'quantidade_participantes', 'quantidade_respostas',
                              'quantidade_pulos',])

        if relatorio.pesquisa:
            pesquisas = Pesquisa.objects.filter(id=relatorio.pesquisa.id)
            filename = "relatorio_por_pesquisa.csv"
        elif relatorio.sistema:
            pesquisas = Pesquisa.objects.filter(acao__sistema=relatorio.sistema)
            filename = "relatorio_por_sistema.csv"
        else:
            pesquisas = Pesquisa.objects.filter(acao__sistema__coordenadoria=relatorio.coordenadoria)
            filename = "relatorio_por_coordenadoria.csv"

        for pesquisa in pesquisas:
            participantes = Usuario.participantes.filter(sistema=pesquisa.acao.sistema)
            media, qnt_respostas, qnt_pulos = get_infos(relatorio, pesquisa)
            escritor_csv.writerow([pesquisa.acao.sistema.coordenadoria.nome,
                                   pesquisa.acao.sistema.nome,
                                   pesquisa,
                                   media,
                                   participantes.count(),
                                   qnt_respostas,
                                   qnt_pulos])

        relatorio.arquivo.save(filename, tmp)
