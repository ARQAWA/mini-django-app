from typing import Any

from app.api.v1.game.schemas import SlotCreatePostBody
from app.core.apps.core.models import Game
from app.core.apps.games.schemas import SlotModelSchema
from app.core.common.ninjas_fix.auth_dep import UserHttpRequest
from app.core.common.ninjas_fix.router import Router
from app.core.services.slots import SlotsService

router = Router(tags=["slots"])


@router.get(
    "/{game_id}/slots",
    summary="Получение слотов игры",
    response={200: list[SlotModelSchema]},
)
async def get_slots(
    request: UserHttpRequest,
    game_id: Game.GAMES_LITERAL,
) -> Any:
    """Получение слотов игры."""
    return await SlotsService().all(request.auth, game_id)


@router.post(
    "/{game_id}/slots",
    summary="Добавление слота игры",
    response={200: SlotModelSchema},
)
async def add_slot(
    request: UserHttpRequest,
    game_id: Game.GAMES_LITERAL,
    body: SlotCreatePostBody,
) -> Any:
    """Добавление слота игры."""
    return await SlotsService().add_slot(request.auth, game_id, body)


@router.patch(
    "/{game_id}/slots/{slot_id}/check_payment",
    summary="Проверка платежа",
    response={200: SlotModelSchema},
)
async def check_payment(
    request: UserHttpRequest,
    game_id: Game.GAMES_LITERAL,
    slot_id: int,
) -> Any:
    """Проверка платежа."""
    return await SlotsService().check_payment(request.auth, game_id, slot_id)


@router.delete(
    "/{game_id}/service_route/slots/{slot_id}",
    summary="Удаление слота игры",
    response={200: None},
    deprecated=True,
)
async def delete_slot(
    request: UserHttpRequest,
    game_id: Game.GAMES_LITERAL,
    slot_id: int,
) -> None:
    """Удаление слота игры."""
    await SlotsService().delete_slot(request.auth, game_id, slot_id)
