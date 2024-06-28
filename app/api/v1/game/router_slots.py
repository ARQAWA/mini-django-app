from typing import Any

from app.api.v1.game.schemas import AccountLinkPutBody, SlotCreatePostBody
from app.core.apps.core.models import Game
from app.core.apps.games.schemas import AccountModelSchema, SlotModelSchema
from app.core.common.ninjas_fix.auth_dep import UserHttpRequest
from app.core.common.ninjas_fix.router import Router
from app.core.services.accounts import AccountsService
from app.core.services.slots import SlotsService

router = Router(tags=["slots"])


@router.get(
    "/{game_hash_name}/slots",
    summary="Получение слотов игры",
    response={200: list[SlotModelSchema]},
)
async def get_slots(
    request: UserHttpRequest,
    game_hash_name: Game.GAMES_LITERAL,
) -> Any:
    """Получение слотов игры."""
    return await SlotsService().all(request.auth, game_hash_name)


@router.post(
    "/{game_hash_name}/slots",
    summary="Добавление слота игры",
    response={200: SlotModelSchema},
)
async def add_slot(
    request: UserHttpRequest,
    game_hash_name: Game.GAMES_LITERAL,
    body: SlotCreatePostBody,
) -> Any:
    """Добавление слота игры."""
    return await SlotsService().add_slot(request.auth, game_hash_name, body.payment_hash)


@router.put(
    "/{game_hash_name}/slots/{slot_id}",
    summary="Привязка/обновление аккаунта в слоте игры",
    response={200: AccountModelSchema},
)
async def link_account(
    request: UserHttpRequest,
    body: AccountLinkPutBody,
    game_hash_name: Game.GAMES_LITERAL,
    slot_id: int,
) -> Any:
    """Привязка/обновление аккаунта в слоте игры."""
    return await AccountsService().link(request.auth, game_hash_name, slot_id, body.init_data, body.proxy)


@router.delete(
    "/{game_hash_name}/slots/{slot_id}",
    summary="Удаление аккаунта из слота игры",
    response={201: None},
)
async def delete_account(
    request: UserHttpRequest,
    game_hash_name: Game.GAMES_LITERAL,
    slot_id: int,
) -> None:
    """Удаление слота игры."""
    await AccountsService().unlink(request.auth, game_hash_name, slot_id)
