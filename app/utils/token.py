from datetime import datetime, timedelta

import jwt
from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


def generate_token(payload: dict, secret: str, expires_in: timedelta) -> str:
    payload["exp"] = datetime.utcnow() + expires_in
    token = str(jwt.encode(payload, secret, algorithm="HS256"))
    return token


def verify_token(token: str, secret: str) -> dict:
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(detail="Token expired", status_code=400)
    except jwt.InvalidTokenError:
        raise HTTPException(detail="Invalid token", status_code=400)


async def get_token(
    authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
):
    return authorization.credentials
