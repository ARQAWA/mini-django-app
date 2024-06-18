from http import HTTPStatus
from typing import Any


class ApiError(Exception):
    """Класс ошибки API."""

    def __init__(self, status: int, message: str, details: Any, with_sentry: bool) -> None:
        self.status = status
        self.message = message
        self.details = details
        self.with_sentry = with_sentry

    @staticmethod
    def __create_error(
        status_code: HTTPStatus,
        message: str | None,
        details: Any,
        with_sentry: bool,
    ) -> "ApiError":
        """Создание ошибки."""
        return ApiError(status_code, message or status_code.phrase, details, with_sentry)

    @classmethod
    def bad_request(
        cls,
        message: str | None = None,
        details: Any = None,
        with_sentry: bool = False,
    ) -> "ApiError":
        """Ошибка запроса."""
        return cls.__create_error(HTTPStatus.BAD_REQUEST, message, details, with_sentry)

    @classmethod
    def unauthorized(
        cls,
        message: str | None = None,
        details: Any = None,
        with_sentry: bool = False,
    ) -> "ApiError":
        """Ошибка авторизации."""
        return cls.__create_error(HTTPStatus.UNAUTHORIZED, message, details, with_sentry)

    @classmethod
    def payment_required(
        cls,
        message: str | None = None,
        details: Any = None,
        with_sentry: bool = False,
    ) -> "ApiError":
        """Ошибка оплаты."""
        return cls.__create_error(HTTPStatus.PAYMENT_REQUIRED, message, details, with_sentry)

    @classmethod
    def forbidden(
        cls,
        message: str | None = None,
        details: Any = None,
        with_sentry: bool = False,
    ) -> "ApiError":
        """Ошибка доступа."""
        return cls.__create_error(HTTPStatus.FORBIDDEN, message, details, with_sentry)

    @classmethod
    def not_found(
        cls,
        message: str | None = None,
        details: Any = None,
        with_sentry: bool = False,
    ) -> "ApiError":
        """Ошибка не найдено."""
        return cls.__create_error(HTTPStatus.NOT_FOUND, message, details, with_sentry)

    @classmethod
    def method_not_allowed(
        cls,
        message: str | None = None,
        details: Any = None,
        with_sentry: bool = False,
    ) -> "ApiError":
        """Ошибка метод не разрешен."""
        return cls.__create_error(HTTPStatus.METHOD_NOT_ALLOWED, message, details, with_sentry)

    @classmethod
    def not_acceptable(
        cls,
        message: str | None = None,
        details: Any = None,
        with_sentry: bool = False,
    ) -> "ApiError":
        """Ошибка неприемлемо."""
        return cls.__create_error(HTTPStatus.NOT_ACCEPTABLE, message, details, with_sentry)

    @classmethod
    def proxy_authentication_required(
        cls,
        message: str | None = None,
        details: Any = None,
        with_sentry: bool = False,
    ) -> "ApiError":
        """Ошибка требуется аутентификация прокси."""
        return cls.__create_error(HTTPStatus.PROXY_AUTHENTICATION_REQUIRED, message, details, with_sentry)

    @classmethod
    def conflict(
        cls,
        message: str | None = None,
        details: Any = None,
        with_sentry: bool = False,
    ) -> "ApiError":
        """Ошибка конфликтов."""
        return cls.__create_error(HTTPStatus.CONFLICT, message, details, with_sentry)

    @classmethod
    def request_timeout(
        cls,
        message: str | None = None,
        details: Any = None,
        with_sentry: bool = False,
    ) -> "ApiError":
        """Ошибка времени ожидания запроса."""
        return cls.__create_error(HTTPStatus.REQUEST_TIMEOUT, message, details, with_sentry)

    @classmethod
    def unprocessable_entity(
        cls,
        message: str | None = None,
        details: Any = None,
        with_sentry: bool = False,
    ) -> "ApiError":
        """Ошибка невыполнимой сущности."""
        return cls.__create_error(HTTPStatus.UNPROCESSABLE_ENTITY, message, details, with_sentry)

    @classmethod
    def too_many_requests(
        cls,
        message: str | None = None,
        details: Any = None,
        with_sentry: bool = False,
    ) -> "ApiError":
        """Ошибка слишком много запросов."""
        return cls.__create_error(HTTPStatus.TOO_MANY_REQUESTS, message, details, with_sentry)

    @classmethod
    def failed_dependency(
        cls,
        message: str | None = None,
        details: Any = None,
        with_sentry: bool = False,
    ) -> "ApiError":
        """Ошибка зависимости не удалась."""
        return cls.__create_error(HTTPStatus.FAILED_DEPENDENCY, message, details, with_sentry)

    @classmethod
    def internal_server_error(
        cls,
        message: str | None = None,
        details: Any = None,
        with_sentry: bool = False,
    ) -> "ApiError":
        """Ошибка внутренней серверной ошибки."""
        return cls.__create_error(HTTPStatus.INTERNAL_SERVER_ERROR, message, details, with_sentry)

    @classmethod
    def not_implemented(
        cls,
        message: str | None = None,
        details: Any = None,
        with_sentry: bool = False,
    ) -> "ApiError":
        """Ошибка не реализовано."""
        return cls.__create_error(HTTPStatus.NOT_IMPLEMENTED, message, details, with_sentry)

    @classmethod
    def service_unavailable(
        cls,
        message: str | None = None,
        details: Any = None,
        with_sentry: bool = False,
    ) -> "ApiError":
        """Ошибка сервис недоступен."""
        return cls.__create_error(HTTPStatus.SERVICE_UNAVAILABLE, message, details, with_sentry)
