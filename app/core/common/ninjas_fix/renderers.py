from typing import Any, cast

import orjson
from django.http import HttpRequest
from ninja import Schema as NinjaSchema
from ninja.renderers import BaseRenderer
from ninja.types import DictStrAny
from pydantic import Field


class Schema(NinjaSchema):
    """Схема API."""

    @classmethod
    def ninja_reponse(cls) -> "type[Schema]":
        """Возвращает класс ответа."""
        return cast(
            type[Schema],
            type(
                f"{cls.__name__}NinjaResponse",
                (Schema,),
                {"__annotations__": cls.ninja_result(cls)},
            ),
        )

    @staticmethod
    def ninja_result(obj: Any) -> DictStrAny:
        """Возвращает результат."""
        return {"error": None, "result": obj}


class ErrorObject(NinjaSchema):
    """Схема ошибки."""

    message: str = Field(description="Сообщение об ошибке")
    details: Any = Field(description="Детали ошибки")


class ErrorResponse(NinjaSchema):
    """Схема ответа с ошибкой."""

    error: ErrorObject = Field(description="Объект ошибки")
    result: None


class ORJSONResponseRenderer(BaseRenderer):
    """Объект обработки возврата API."""

    media_type = "application/json"

    def render(self, request: HttpRequest, data: Any, *, response_status: int) -> bytes:
        """Функция обработчик."""
        return orjson.dumps(data, default=str)
