from ninja import Router

from app.api.v1.user.schemas import MePostBody, TgAuthResponse
from app.core.common.auth_request import HttpRequest
from app.core.models.tg_user_data import PlayerData
from app.core.services.auth import AuthService

router = Router(tags=["auth"])


@router.post(
    "/auth",
    summary="Авторизация через телеграм",
    response={200: TgAuthResponse},
    auth=None,
)
async def user_authorize(request: HttpRequest, body: MePostBody) -> dict[str, str]:
    """Ручка для авторизации пользователя через телеграм."""
    return {
        "token": await AuthService().authorize(
            body.init_data,
            user_agent=request.headers.get("User-Agent", "Unknown"),
        )
    }


@router.get(
    "/me",
    summary="Получение информации о текущем пользователе",
    response={200: PlayerData},
)
async def get_user_info(request: HttpRequest) -> PlayerData.Dict:
    """Ручка для получения информации о текущем пользователе."""
    return request.auth
