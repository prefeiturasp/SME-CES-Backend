import jwt
import datetime
from django.conf import settings
from django.core.exceptions import ValidationError


def gerar_jwt_token(user_UUID, pesquisa_UUID):

    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)

    payload = {
        'user_uuid': str(user_UUID),
        'pesquisa_uuid': str(pesquisa_UUID),
        'exp': expiration_time,
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    return token


def decodificar_jwt_token(token):

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

        user = payload['user_uuid']
        pesquisa = payload['pesquisa_uuid']

        return {
            'user_uuid': user,
            'pesquisa_uuid': pesquisa,
        }

    except jwt.ExpiredSignatureError:
        raise ValidationError(message='Token expirou.')
    except jwt.DecodeError:
        raise ValidationError(message='Token inválido.')
