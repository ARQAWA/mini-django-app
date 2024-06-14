from django.http import HttpRequest
from ninja import Router

from app.api.v1.schemas import MePostBody
from app.core.services.auth import process_user_auth
from app.logic.tg_auth_validation import TgUser, TgUserSchema

router = Router(tags=["auth"])


@router.post(
    "/me",
    summary="Информация о текущем пользователе",
    description="Ручка для получения информации о текущем пользователе.",
    response={200: TgUserSchema},
)
async def me_post(request: HttpRequest, body: MePostBody) -> TgUser:
    """Ручка для получения информации о текущем пользователе."""
    user_object = await process_user_auth(body.init_data)

    return user_object
