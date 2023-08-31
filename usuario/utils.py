from django.contrib.auth.models import Group, Permission
from usuario.constants import GRUPO_NIVEL_PO, GRUPO_NIVEL_COORDENADORIA

ALL = ['view', 'add', 'change', 'delete']


def atribuir_permissao(grupo, settings):
    verb_options = ['add', 'change', 'delete', 'view']

    for key in settings:
        verbs_by_key = settings[key]

        for permission in Permission.objects.all():
            for verb in verb_options:
                if (verb + key == permission.codename) and verb in verbs_by_key:
                    grupo.permissions.add(permission)
                    print('Permissão adicionada ao grupo {} => {}'.format(grupo, permission.codename))


def setup_grupos_e_permissoes():
    '''Cria grupos e atribui permissões.'''

    # coordenador = ['sistema', 'acao', 'relatorios', 'usuario']
    # po = ['acao', 'relatorios']

    permissions = Permission.objects.all()
    for item in permissions:
        print(item.codename)

    coordenador, _ = Group.objects.get_or_create(name=GRUPO_NIVEL_COORDENADORIA)
    coordenador_settings = {
        '_sistema': ALL,
        '_acao': ALL,
        '_usuario': ALL,
    }
    atribuir_permissao(coordenador, coordenador_settings)

    po, _ = Group.objects.get_or_create(name=GRUPO_NIVEL_PO)
    po_settings = {
        '_acao': ALL,
        '_sistema': ['view']
    }
    atribuir_permissao(po, po_settings)
