import jwt


def generate_token(payload: dict, secret: str, expires_in: float) -> str:
    payload['exp'] = expires_in
    token = str(jwt.encode(payload, secret, algorithm='HS256'))
    return token
