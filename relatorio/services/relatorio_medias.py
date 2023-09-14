import csv
from django.db.models import Sum
from tempfile import NamedTemporaryFile
from pesquisa.models import Pesquisa


def get_infos(relatorio, pesquisa):
    tokens_com_resposta = pesquisa.tokens.filter(resposta__isnull=False,
                                                 resposta__criado_em__gte=relatorio.periodo_inicio,
                                                 resposta__criado_em__lte=relatorio.periodo_fim)

    total_ocorrencias = 0
    for peso in [1, 2, 3, 4, 5, 6, 7]:
        total_ocorrencias += tokens_com_resposta.filter(resposta__nota=peso).count() * peso

    try:
        media = total_ocorrencias/tokens_com_resposta.count()
    except Exception:
        media = 0

    qnt_respostas = tokens_com_resposta.count()
    qnt_pulos = pesquisa.tokens.aggregate(total=Sum('pulos'))['total']

    return media, qnt_respostas, qnt_pulos


def gerar_csv(relatorio):
    with NamedTemporaryFile(mode="r+", prefix='relatorio', suffix='.csv') as tmp:
        escritor_csv = csv.writer(tmp.file, delimiter=";")

        escritor_csv.writerow(['coordenadoria', 'sistema', 'pesquisa', 'media', 'quantidade_respostas',
                              'quantidade_pulos',])

        if relatorio.pesquisa:
            pesquisas = Pesquisa.objects.filter(id=relatorio.pesquisa.id)
            filename = "relatorio_por_pesquisa.csv"
        if relatorio.sistema:
            pesquisas = Pesquisa.objects.filter(acao__sistema=relatorio.sistema)
            filename = "relatorio_por_sistema.csv"
        if relatorio.coordenadoria:
            pesquisas = Pesquisa.objects.filter(acao__sistema__coordenadoria=relatorio.coordenadoria)
            filename = "relatorio_por_coordenadoria.csv"

        for pesquisa in pesquisas:
            media, qnt_respostas, qnt_pulos = get_infos(relatorio, pesquisa)
            escritor_csv.writerow([pesquisa.acao.sistema.coordenadoria.nome,
                                   pesquisa.acao.sistema.nome,
                                   pesquisa,
                                   media,
                                   qnt_respostas,
                                   qnt_pulos])

        relatorio.arquivo.save(filename, tmp)
