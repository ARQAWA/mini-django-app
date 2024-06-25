from django.http import HttpRequest
from ninja.types import DictStrAny

from app.api.v1.user.schemas import AuthHashPostBody, RefreshTokenPostBody, TgAuthResponse
from app.core.common.ninjas_fix.auth_dep import UserHttpRequest
from app.core.common.ninjas_fix.router import Router
from app.core.models.user_data import UserData
from app.core.services.web_auth import WebAuthService

router = Router(tags=["auth"])


@router.post(
    "/auth",
    summary="Авторизация через hash авторизации",
    response={200: TgAuthResponse.ninja_reponse()},
    auth=None,
)
async def user_authorize(request: HttpRequest, body: AuthHashPostBody) -> DictStrAny:
    """Ручка для авторизации пользователя через телеграм."""
    access, refresh = await WebAuthService().authorize(body.hash)
    return TgAuthResponse.ninja_result({"access": access, "refresh": refresh})


@router.post(
    "/refresh",
    summary="Обновление токена",
    response={200: TgAuthResponse.ninja_reponse()},
    auth=None,
)
async def user_refresh(request: HttpRequest, body: RefreshTokenPostBody) -> DictStrAny:
    """Ручка для авторизации пользователя через телеграм."""
    access, refresh = await WebAuthService().refresh(body.token)
    return TgAuthResponse.ninja_result({"access": access, "refresh": refresh})


@router.get(
    "/me",
    summary="Получение информации о текущем пользователе",
    response={200: UserData.ninja_reponse()},
)
async def get_user_info(request: UserHttpRequest) -> DictStrAny:
    """Ручка для получения информации о текущем пользователе."""
    return UserData.ninja_result(request.auth)
