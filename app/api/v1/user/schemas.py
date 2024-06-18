from ninja import Schema
from pydantic import Field


class MePostBody(Schema):
    """Схема тела запроса."""

    init_data: str = Field(alias="initData", description="Инициализационные данные")


class TgAuthResponse(Schema):
    """Схема ответа авторизации."""

    token: str = Field(alias="token", description="Токен авторизации")
