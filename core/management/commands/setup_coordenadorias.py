from django.core.management.base import BaseCommand
from core.models import Coordenadoria


class Command(BaseCommand):
    help = '''Cria coordenadorias iniciais'''

    def handle(self, *args, **options):
        coordenadorias = [
            "COTIC",
            "COPED",
            "CODAE",
            "COPLAN",
            "COCEU",
            "COGEP",
            "COMPS",
            "COMAPRE",
            "COSERV",
            "CONT",
            "ASCOM",
            "AJ",
            "ASPAR",
            "NUTAC",
            "Núcleo Administrativo"
        ]

        for nome in coordenadorias:
            Coordenadoria.objects.get_or_create(sigla=nome, defaults={'nome': nome})
