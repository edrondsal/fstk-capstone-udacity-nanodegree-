import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from responses import AppError

AUTH0_DOMAIN = 'fsnder.eu.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'castingagencyapi'

def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AppError(status_code= 401, title= 'authorization_header_missing',detail='Authorization header is expected.')
    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AppError(status_code= 401, title= 'invalid_header',detail= 'Authorization header must start with "Bearer".')
    elif len(parts) == 1:
        raise AppError(status_code= 401, title= 'invalid_header',detail= 'Toke not found.')
    elif len(parts) > 2:
        raise AppError(status_code= 401, title= 'invalid_header',detail= 'Authorization header must be bearer token.')
    token = parts[1]
    return token

def verify_decode_jwt(token):
    unverified_header = jwt.get_unverified_header(token)
    if 'kid' not in unverified_header:
        raise AppError(status_code= 401, title= 'invalid_header',detail= 'Authorization malformed.')

    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())    
    rsa_key = {}
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AppError(status_code= 401, title= 'token_expired',detail='Token expired.')
        except jwt.JWTClaimsError:
            raise AppError(status_code= 401, title= 'invalid_claims',detail='Incorrect claims. Please, check the audience and issuer.')
        except Exception:
            raise AppError(status_code= 400,title='invalid_header',detail='Unable to parse authentication token.')
    raise AppError(status_code= 400,title='invalid_header',detail='Unable to find the appropriate key.')

def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AppError(status_code= 400,title='invalid_claims',detail='Permissions not included in JWT.')
    if permission not in payload['permissions']:
        raise AppError(status_code= 401,title='unauthorized',detail='Permission not found.')
    return True

def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator