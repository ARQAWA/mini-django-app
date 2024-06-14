from django.http import HttpRequest, HttpResponse
from ninja import NinjaAPI
from ninja.errors import ValidationError

from app.logic.tg_auth_validation import TgAuthError


def setup_exception_handlers(api: NinjaAPI) -> None:
    """Установка обработчиков исключений."""

    @api.exception_handler(Exception)
    def internal_error(request: HttpRequest, _err: Exception) -> HttpResponse | HttpResponse:
        return api.create_response(
            request,
            {
                "error": {
                    "message": "Internal Server Error",
                    "details": None,
                },
                "result": None,
            },
            status=500,
        )

    @api.exception_handler(TgAuthError)
    def tg_auth_error(request: HttpRequest, err: TgAuthError) -> HttpResponse | HttpResponse:
        return api.create_response(
            request,
            {
                "error": {
                    "message": "Telegram Auth Error",
                    "details": None,
                },
                "result": None,
            },
            status=401,
        )

    @api.exception_handler(ValidationError)
    def request_validation_error(request: HttpRequest, err: ValidationError) -> HttpResponse | HttpResponse:
        return api.create_response(
            request,
            {
                "error": {
                    "message": "Request Validation Error",
                    "details": err.errors,
                },
                "result": None,
            },
            status=422,
        )
