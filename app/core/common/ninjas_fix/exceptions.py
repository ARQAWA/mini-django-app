from http import HTTPStatus
from typing import Any

import orjson
import sentry_sdk
from django.http import HttpRequest, HttpResponse
from ninja import NinjaAPI
from ninja.errors import ValidationError

from app.core.common.error import ApiError


def setup_exception_handlers(api: NinjaAPI) -> None:
    """Установка обработчиков исключений."""

    # noinspection PyUnusedLocal
    @api.exception_handler(ApiError)
    def api_error(request: HttpRequest, err: ApiError) -> HttpResponse:
        if err.with_sentry:
            sentry_sdk.capture_exception(err)

        return __get_response(err.status, err.message, err.details)

    # noinspection PyUnusedLocal
    @api.exception_handler(ValidationError)
    def request_validation_error(request: HttpRequest, err: ValidationError) -> HttpResponse:
        return __get_response(HTTPStatus.UNPROCESSABLE_ENTITY, "Request Validation Error", err.errors)

    # noinspection PyUnusedLocal
    @api.exception_handler(Exception)
    def internal_error(request: HttpRequest, err: Exception) -> HttpResponse:
        sentry_sdk.capture_exception(err)
        return __get_response(HTTPStatus.INTERNAL_SERVER_ERROR, HTTPStatus.INTERNAL_SERVER_ERROR.phrase)


def __get_response(
    status: int,
    message: str,
    details: Any = None,
) -> HttpResponse:
    """Получение ответа API."""
    return HttpResponse(
        content=orjson.dumps(
            {
                "error": {
                    "message": message,
                    "details": details,
                },
            },
            default=str,
        ),
        status=status,
        content_type="application/json",
        charset="utf-8",
    )
