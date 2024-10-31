from django.http import HttpRequest
from django.http import HttpRequest as DjangoHttpRequest
from ninja.security.base import SecuritySchema

from app.core.common.error import UNATHORIZED_ERROR
from app.core.envs import envs
from app.core.services.web_auth import WebAuthService

SECURITY_SCHEMA = SecuritySchema(type="http", scheme="bearer")


def _extract_token(request: HttpRequest) -> str:
    """Извлечение токена из запроса."""
    if (
        (token := request.headers.get("Authorization", None)) is None
        or not isinstance(token, str)
        or not (token := token.strip()).startswith("Bearer ")
        or not (token := token[7:].strip())
    ):
        raise UNATHORIZED_ERROR

    return token


class UserHttpRequest(DjangoHttpRequest):
    """Класс для запроса с объектом авторизации."""

    auth: int


class UserAuthDepends:
    """Класс для получения объекта пользователя из токена."""

    openapi_security_schema = SECURITY_SCHEMA

    async def __call__(self, request: HttpRequest) -> int:
        """Получение объекта пользователя из заголовка Authorization."""
        token = _extract_token(request)

        if (user_id := await WebAuthService().get_user_id_by_access(token)) is None:
            raise UNATHORIZED_ERROR

        return user_id


class BrosSecretAuthDepends:
    """Класс для секретного ключа."""

    openapi_security_schema = SECURITY_SCHEMA

    def __call__(self, request: HttpRequest) -> int:
        """Проверка секретного ключа."""
        token = _extract_token(request)

        if token != envs.bros_secret_token:
            raise UNATHORIZED_ERROR

        return 1


__all__ = ["UserAuthDepends", "UserHttpRequest", "BrosSecretAuthDepends", "UNATHORIZED_ERROR"]
