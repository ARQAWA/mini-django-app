from typing import Any

from django.http import HttpRequest

from app.api.v1.user.schemas import AuthHashPostBody, RefreshTokenPostBody, TgAuthResponse
from app.core.apps.users.schemas import CustomerModelSchema
from app.core.common.ninjas_fix.auth_dep import UserHttpRequest
from app.core.common.ninjas_fix.router import Router
from app.core.services.auth.web_auth import WebAuthService

router = Router(tags=["auth"])


@router.get(
    "/me",
    summary="Получение информации о текущем пользователе",
    response={200: CustomerModelSchema},
)
async def get_user_info(request: UserHttpRequest) -> Any:
    """Ручка для получения информации о текущем пользователе."""
    return await WebAuthService().get_user_by_id(request.auth)


@router.post(
    "/auth",
    summary="Авторизация через hash авторизации",
    response={200: TgAuthResponse},
    auth=None,
)
async def user_authorize(
    request: HttpRequest,
    body: AuthHashPostBody,
) -> Any:
    """Ручка для авторизации пользователя через телеграм."""
    access, refresh = await WebAuthService().authorize(body.hash)
    return dict(access=access, refresh=refresh)


@router.post(
    "/refresh",
    summary="Обновление токена",
    response={200: TgAuthResponse},
    auth=None,
)
async def user_refresh(
    request: HttpRequest,
    body: RefreshTokenPostBody,
) -> Any:
    """Ручка для авторизации пользователя через телеграм."""
    access, refresh = await WebAuthService().refresh(body.token)
    return dict(access=access, refresh=refresh)
