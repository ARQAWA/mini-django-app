from django.http import HttpRequest
from ninja.security.base import SecuritySchema

from app.core.error import ApiError
from app.core.models.tg_user_data import PlayerData
from app.core.repositories.user import UserRepository

UNATHORIZED_ERROR = ApiError.unauthorized()


async def player_auth(request: HttpRequest) -> PlayerData.Dict:
    """Получение заголовка Authorization."""
    if (
        (token := request.headers.get("Authorization", None)) is None
        or not isinstance(token, str)
        or not (token := token.strip()).startswith("Bearer ")
        or not (token := token[7:].strip())
    ):
        raise UNATHORIZED_ERROR

    if (user := await UserRepository().get_user(token)) is None:
        raise UNATHORIZED_ERROR

    return user


setattr(player_auth, "openapi_security_schema", SecuritySchema(type="http", scheme="bearer"))

__all__ = ["player_auth"]
