from django.http import HttpRequest
from django.http import HttpRequest as DjangoHttpRequest
from ninja.security.base import SecuritySchema

from app.core.apps.users.schemas import CustomerSchema
from app.core.common.error import UNATHORIZED_ERROR
from app.core.services.auth.web_auth import WebAuthService

SECURITY_SCHEMA = SecuritySchema(type="http", scheme="bearer")


class UserHttpRequest(DjangoHttpRequest):
    """Класс для запроса с объектом авторизации."""

    auth: CustomerSchema


class UserAuthDepends:
    """Класс для получения объекта пользователя из токена."""

    openapi_security_schema = SECURITY_SCHEMA

    async def __call__(self, request: HttpRequest) -> CustomerSchema:
        """Получение объекта пользователя из заголовка Authorization."""
        if (
            (token := request.headers.get("Authorization", None)) is None
            or not isinstance(token, str)
            or not (token := token.strip()).startswith("Bearer ")
            or not (token := token[7:].strip())
        ):
            raise UNATHORIZED_ERROR

        user = await WebAuthService().get_user_by_access(token)
        if user is None:
            raise UNATHORIZED_ERROR

        return CustomerSchema.model_construct(
            id=user["id"],
            first_name=user["first_name"],
            last_name=user["last_name"],
            username=user["username"],
            has_trial=user["has_trial"],
        )


__all__ = ["UserAuthDepends", "UserHttpRequest", "UNATHORIZED_ERROR"]
