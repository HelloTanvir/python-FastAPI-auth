from fastapi.exceptions import HTTPException
from pydantic import BaseModel, validate_email, validator

from app.db.db import db


class SignupDto(BaseModel):
    name: str
    email: str
    password: str

    @validator("email")
    def email_must_be_valid(cls, value):
        if validate_email(value):
            user = db.users.find_one({"email": value})

            if user:
                raise HTTPException(detail="Email already exists", status_code=400)

            return value

    @validator("password")
    def password_must_be_at_least_6_characters_long(cls, value):
        if len(value) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return value

class LoginDto(BaseModel):
    email: str
    password: str

    @validator("email")
    def email_must_be_valid(cls, value):
        if validate_email(value):
            return value

    @validator("password")
    def password_must_be_at_least_6_characters_long(cls, value):
        if len(value) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return value

class RefreshTokensDto(BaseModel):
    refresh_token: str