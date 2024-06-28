from django.http import HttpRequest
from django.http import HttpRequest as DjangoHttpRequest
from ninja.security.base import SecuritySchema

from app.core.common.error import UNATHORIZED_ERROR
from app.core.services.web_auth import WebAuthService

SECURITY_SCHEMA = SecuritySchema(type="http", scheme="bearer")


class UserHttpRequest(DjangoHttpRequest):
    """Класс для запроса с объектом авторизации."""

    auth: int


class UserAuthDepends:
    """Класс для получения объекта пользователя из токена."""

    openapi_security_schema = SECURITY_SCHEMA

    async def __call__(self, request: HttpRequest) -> int:
        """Получение объекта пользователя из заголовка Authorization."""
        if (
            (token := request.headers.get("Authorization", None)) is None
            or not isinstance(token, str)
            or not (token := token.strip()).startswith("Bearer ")
            or not (token := token[7:].strip())
        ):
            raise UNATHORIZED_ERROR

        user_id = await WebAuthService().get_user_id_by_access(token)

        if user_id is None:
            raise UNATHORIZED_ERROR

        return user_id


__all__ = ["UserAuthDepends", "UserHttpRequest", "UNATHORIZED_ERROR"]
