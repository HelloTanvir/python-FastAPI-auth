import os
from datetime import datetime, timedelta

from fastapi.exceptions import HTTPException

from app.db.db import db
from app.utils.auth_dto import LoginDto, SignupDto
from app.utils.auth_response import Tokens
from app.utils.generate_token import generate_token


def signup(body: SignupDto) -> Tokens:
    user = body.dict()

    # set initial refresh_token of the user empty
    user["refresh_token"] = ""

    result = db.users.insert_one(user)

    # generate access token
    access_token_expires = (datetime.utcnow() + timedelta(minutes=15)).timestamp()
    access_token_secret = os.environ["AT_SECRET_KEY"]
    access_token = generate_token({'id': str(result.inserted_id)}, access_token_secret, access_token_expires)

    # generate refresh token
    refresh_token_expires = (datetime.utcnow() + timedelta(weeks=1)).timestamp()
    refresh_token_secret = os.environ["RT_SECRET_KEY"]
    refresh_token = generate_token({'id': str(result.inserted_id)}, refresh_token_secret, refresh_token_expires)

    # update refresh token in db
    db.users.update_one({'_id': result.inserted_id}, {'$set': {'refresh_token': refresh_token}})

    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }


def login(body: LoginDto) -> Tokens:
    user = db.users.find_one({'email': body.email})

    if not user:
        raise HTTPException(detail="User not found", status_code=400)

    if user['password'] != body.password:
        raise HTTPException(detail="Incorrect password", status_code=400)

    # generate access token
    access_token_expires = (datetime.utcnow() + timedelta(minutes=15)).timestamp()
    access_token_secret = os.environ["AT_SECRET_KEY"]
    access_token = generate_token({'id': str(user['_id'])}, access_token_secret, access_token_expires)

    # generate refresh token
    refresh_token_expires = (datetime.utcnow() + timedelta(weeks=1)).timestamp()
    refresh_token_secret = os.environ["RT_SECRET_KEY"]
    refresh_token = generate_token({'id': str(user['_id'])}, refresh_token_secret, refresh_token_expires)

    # update refresh token in db
    db.users.find_one_and_update({'_id': user['_id']}, {'$set': {'refresh_token': refresh_token}})

    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }