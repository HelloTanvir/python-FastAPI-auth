from pydantic import BaseModel, validate_email, validator


class SignupDto(BaseModel):
    name: str
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