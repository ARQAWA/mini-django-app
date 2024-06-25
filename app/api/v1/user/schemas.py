from typing import TypedDict

from pydantic import Field

from app.core.common.ninjas_fix.renderers import Schema


class AuthHashPostBody(Schema):
    """Схема тела запроса авторизации."""

    hash: str = Field(description="Hash авторизации")


class RefreshTokenPostBody(Schema):
    """Схема тела запроса авторизации."""

    token: str = Field(description="Токен обновления")


class TgAuthResponse(Schema):
    """Схема ответа авторизации."""

    access: str = Field(description="Токен доступа")
    refresh: str = Field(description="Токен обновления")

    class Dict(TypedDict):
        """Типизация ответа авторизации."""

        access: str
        refresh: str
