"""This module provides the DTOs for authentication"""
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, validate_email, validator

from app.db.db import db


class SignupDto(BaseModel):
    """This class provides the DTO for signup"""

    name: str
    email: str
    password: str

    @validator("email")
    # pylint: disable=no-self-argument
    def email_must_be_valid(cls, value):
        """This method validates the email"""
        if validate_email(value):
            user = db.users.find_one({"email": value})

            if user:
                raise HTTPException(
                    detail="Email already exists", status_code=400
                )

            return value

    @validator("password")
    # pylint: disable=no-self-argument
    def password_must_be_at_least_6_characters_long(cls, value):
        """This method validates the password"""
        if len(value) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return value


class LoginDto(BaseModel):
    """This class provides the DTO for login"""

    email: str
    password: str

    @validator("email")
    # pylint: disable=no-self-argument
    def email_must_be_valid(cls, value):
        """This method validates the email"""
        if validate_email(value):
            return value

    @validator("password")
    # pylint: disable=no-self-argument
    def password_must_be_at_least_6_characters_long(cls, value):
        """This method validates the password"""
        if len(value) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return value


class RefreshTokensDto(BaseModel):
    """This class provides the DTO for refresh tokens"""
    refresh_token: str
