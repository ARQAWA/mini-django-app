from typing import Any

import orjson
from django.http import HttpRequest
from ninja import Schema as NinjaSchema
from ninja.renderers import BaseRenderer
from pydantic import Field


class ErrorObject(NinjaSchema):
    """Схема ошибки."""

    message: str = Field(title="Сообщение об ошибке")
    details: Any = Field(title="Детали ошибки")


class ErrorResponse(NinjaSchema):
    """Схема ответа с ошибкой."""

    error: ErrorObject = Field(title="Объект ошибки")


class ORJSONResponseRenderer(BaseRenderer):
    """Объект обработки возврата API."""

    media_type = "application/json"

    def render(self, request: HttpRequest, data: Any, *, response_status: int) -> bytes:
        """Функция обработчик."""
        return orjson.dumps(data, default=str)
