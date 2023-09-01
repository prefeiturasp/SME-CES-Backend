from django.contrib.auth.models import Group, Permission
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from usuario.constants import GRUPO_NIVEL_PO, GRUPO_NIVEL_COORDENADORIA
from ces.utils import email_utils

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
        '_pesquisa': ALL
    }
    atribuir_permissao(coordenador, coordenador_settings)

    po, _ = Group.objects.get_or_create(name=GRUPO_NIVEL_PO)
    po_settings = {
        '_acao': ALL,
        '_sistema': ['view'],
        '_pesquisa': ALL
    }
    atribuir_permissao(po, po_settings)


def envia_email_novo_usuario(usuario):
    password_reset_link = gerar_url_redefinicao_senha(usuario)
    subject = '[CES] Instruções primeiro acesso.'
    dict = {
        'subject': '[CES] Instruções primeiro acesso.',
        'admin_url': settings.ADMIN_URL,
        'password_reset_link': password_reset_link,
    }
    email_utils.send_email_ctrl(
        subject,
        dict,
        'email/primeiro_acesso.html',
        [usuario.email]
    )


def gerar_url_redefinicao_senha(usuario):
    token = default_token_generator.make_token(usuario)
    uid = urlsafe_base64_encode(force_bytes(usuario.pk))
    return f"{settings.ADMIN_URL}/reset/{uid}/{token}/"
