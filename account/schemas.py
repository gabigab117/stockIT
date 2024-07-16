import re
from ninja import Schema
from pydantic import field_validator, EmailStr, Field


class RegisterSchema(Schema):
    username: str
    email: EmailStr
    last_name: str  # | None = None
    first_name: str  # | None = None
    password: str  # = Field(min_length=8)
    password2: str

    # @field_validator('password')
    # def password_length(cls, v: str):
    #     if len(v) < 8:
    #         raise ValueError('Le mot de passe doit contenir au moins 8 caractères.')
    #     return v

    @field_validator('password')
    def password_strength(cls, v: str):
        if not re.search(r'^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%_^&*?]).*$', v):
            raise ValueError(
                'Le mot de passe doit contenir au moins 8 caractères, une majuscule, une minuscule, '
                'un chiffre et un caractère spécial.')
        return v


class LoginSchema(Schema):
    email: EmailStr
    password: str
