import os
from datetime import timedelta

from bson import ObjectId
from fastapi.exceptions import HTTPException
from passlib.hash import pbkdf2_sha256

from app.db.db import db
from app.utils.auth_dto import LoginDto, RefreshTokensDto, SignupDto
from app.utils.auth_response import Tokens
from app.utils.token import generate_token, verify_token


def signup(body: SignupDto) -> Tokens:
    user = body.dict()

    # set initial refresh_token of the user empty
    user["refresh_token"] = ""

    # hash password
    user["password"] = pbkdf2_sha256.hash(user["password"])

    result = db.users.insert_one(user)

    # generate access token
    access_token_expires = timedelta(minutes=15)
    access_token_secret = os.environ["AT_SECRET_KEY"]
    access_token = generate_token(
        {"id": str(result.inserted_id)}, access_token_secret, access_token_expires
    )

    # generate refresh token
    refresh_token_expires = timedelta(weeks=1)
    refresh_token_secret = os.environ["RT_SECRET_KEY"]
    refresh_token = generate_token(
        {"id": str(result.inserted_id)}, refresh_token_secret, refresh_token_expires
    )

    # update refresh token in db
    db.users.update_one(
        {"_id": result.inserted_id}, {"$set": {"refresh_token": refresh_token}}
    )

    return {"access_token": access_token, "refresh_token": refresh_token}


def login(body: LoginDto) -> Tokens:
    user = db.users.find_one({"email": body.email})

    if not user:
        raise HTTPException(detail="User not found", status_code=400)

    # verify password
    if not pbkdf2_sha256.verify(body.password, user["password"]):
        raise HTTPException(detail="Incorrect password", status_code=400)

    # generate access token
    access_token_expires = timedelta(minutes=15)
    access_token_secret = os.environ["AT_SECRET_KEY"]
    access_token = generate_token(
        {"id": str(user["_id"])}, access_token_secret, access_token_expires
    )

    # generate refresh token
    refresh_token_expires = timedelta(weeks=1)
    refresh_token_secret = os.environ["RT_SECRET_KEY"]
    refresh_token = generate_token(
        {"id": str(user["_id"])}, refresh_token_secret, refresh_token_expires
    )

    # update refresh token in db
    db.users.find_one_and_update(
        {"_id": user["_id"]}, {"$set": {"refresh_token": refresh_token}}
    )

    return {"access_token": access_token, "refresh_token": refresh_token}


def refresh_tokens(id: str, body: RefreshTokensDto) -> Tokens:
    user = db.users.find_one({"_id": ObjectId(id)})

    if not user:
        raise HTTPException(detail="User not found", status_code=400)

    # verify refresh token
    refresh_token_secret = os.environ["RT_SECRET_KEY"]
    if not verify_token(body.refresh_token, refresh_token_secret):
        raise HTTPException(detail="Invalid refresh token", status_code=400)

    # generate access token
    access_token_expires = timedelta(minutes=15)
    access_token_secret = os.environ["AT_SECRET_KEY"]
    access_token = generate_token(
        {"id": str(user["_id"])}, access_token_secret, access_token_expires
    )

    # generate refresh token
    refresh_token_expires = timedelta(weeks=1)
    refresh_token = generate_token(
        {"id": str(user["_id"])}, refresh_token_secret, refresh_token_expires
    )

    # update refresh token in db
    db.users.find_one_and_update(
        {"_id": user["_id"]}, {"$set": {"refresh_token": refresh_token}}
    )

    return {"access_token": access_token, "refresh_token": refresh_token}
