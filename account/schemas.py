from ninja import Schema
from pydantic import field_validator, EmailStr, Field

from django.conf import settings


class RegisterSchema(Schema):
    username: str
    email: EmailStr
    last_name: str  # | None = None
    first_name: str  # | None = None
    password: str = Field(min_length=8)
    password2: str

    # @field_validator('password')
    # def password_length(cls, v: str):
    #     if len(v) < 8:
    #         raise ValueError('Le mot de passe doit contenir au moins 8 caractères.')
    #     return v

    @field_validator('password')
    def password_strength(cls, v: str):
        if not any(char.isdigit() for char in v):
            raise ValueError('Le mot de passe doit contenir au moins un chiffre.')
        if not any(char.isupper() for char in v):
            raise ValueError('Le mot de passe doit contenir au moins une majuscule.')
        if not any(char in settings.SPECIAL_CHARS for char in v):
            raise ValueError(f'Le mot de passe doit contenir au moins un caractère spécial : {settings.SPECIAL_CHARS}.')
        return v
