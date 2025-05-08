from functools import wraps
from flask import request, jsonify
import jwt
import requests
import os

COGNITO_REGION = os.getenv('COGNITO_REGION')
COGNITO_USER_POOL_ID = os.getenv('COGNITO_USER_POOL_ID')
COGNITO_ISSUER = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}"

# Descargar y cachear las claves públicas de Cognito
JWKS_URL = f"{COGNITO_ISSUER}/.well-known/jwks.json"
jwks = requests.get(JWKS_URL).json()

def get_public_key(token):
    headers = jwt.get_unverified_header(token)
    kid = headers['kid']
    key = next((k for k in jwks['keys'] if k['kid'] == kid), None)
    if not key:
        raise Exception('Clave pública no encontrada.')
    return jwt.algorithms.RSAAlgorithm.from_jwk(key)

def require_jwt(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization', None)
        if not auth_header:
            return jsonify({"error": "Token no proporcionado."}), 401

        try:
            token = auth_header.split(" ")[1]  # Formato: Bearer TOKEN
            public_key = get_public_key(token)
            decoded_token = jwt.decode(
                token,
                public_key,
                algorithms=['RS256'],
                audience=os.getenv('COGNITO_APP_CLIENT_ID'),
                issuer=COGNITO_ISSUER
            )
            # Opcional: puedes guardar el decoded_token en flask.g si quieres usar info de usuario
        except Exception as e:
            return jsonify({"error": f"Token inválido: {str(e)}"}), 401

        return f(*args, **kwargs)
    return decorated_function
