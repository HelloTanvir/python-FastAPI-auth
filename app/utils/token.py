"""This module provides necessary functions for working with tokens"""
from datetime import datetime, timedelta

import jwt
from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


def generate_token(payload: dict, secret: str, expires_in: timedelta) -> str:
    """This function generates a token"""
    payload["exp"] = datetime.utcnow() + expires_in
    token = str(jwt.encode(payload, secret, algorithm="HS256"))
    return token


def verify_token(token: str, secret: str) -> dict:
    """This function verifies a token"""
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError as expired_exception:
        raise HTTPException(
            detail="Token expired", status_code=400
        ) from expired_exception
    except jwt.InvalidTokenError as invalid_exception:
        raise HTTPException(
            detail="Invalid token", status_code=400
        ) from invalid_exception


async def get_token(
    authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
):
    """This function extracts token from authorization header and returns it"""
    return authorization.credentials
