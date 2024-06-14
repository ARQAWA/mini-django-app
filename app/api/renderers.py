from typing import Any

import orjson
from django.http import HttpRequest
from ninja.renderers import BaseRenderer


class ORJSONResponseRenderer(BaseRenderer):
    """Объект обработки возврата API."""

    media_type = "application/json"

    def render(self, request: HttpRequest, data: Any, *, response_status: int) -> bytes:
        """Функция обработчик."""
        return orjson.dumps(
            {
                "errors": {},
                "data": data,
            },
            default=str,
        )


class ORJSONErrorRenderer(BaseRenderer):
    """Объект обработки ошибок API."""

    media_type = "application/json"

    def render(self, request: HttpRequest, data: Any, *, response_status: int) -> bytes:
        """Функция обработчик."""
        return orjson.dumps(
            {
                "errors": data,
                "data": {},
            },
            default=str,
        )
