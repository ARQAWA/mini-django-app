from ninja import Schema
from pydantic import Field


class AuthHashPostBody(Schema):
    """Схема тела запроса авторизации."""

    hash: str = Field(title="Hash авторизации")


class RefreshTokenPostBody(Schema):
    """Схема тела запроса авторизации."""

    token: str = Field(title="Токен обновления")


class TgAuthResponse(Schema):
    """Схема ответа авторизации."""

    access: str = Field(title="Токен доступа")
    refresh: str = Field(title="Токен обновления")
