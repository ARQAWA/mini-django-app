from typing import Any

from app.api.v1.game.schemas import AccountLinkPutBody, AccountSwitchPlayPostBody
from app.core.apps.core.models import Game
from app.core.apps.games.schemas import AccountModelSchema
from app.core.common.ninjas_fix.auth_dep import UserHttpRequest
from app.core.common.ninjas_fix.router import Router
from app.core.services.accounts import AccountsService

router = Router(tags=["accounts"])


@router.put(
    "/{game_id}/slots/{slot_id}",
    summary="Привязка/обновление аккаунта в слоте игры",
    response={200: AccountModelSchema},
)
async def link_account(
    request: UserHttpRequest,
    body: AccountLinkPutBody,
    game_id: Game.GAMES_LITERAL,
    slot_id: int,
) -> Any:
    """Привязка/обновление аккаунта в слоте игры."""
    return await AccountsService().link(request.auth, game_id, slot_id, body)


@router.delete(
    "/{game_id}/slots/{slot_id}",
    summary="Удаление аккаунта из слота игры",
    response={200: None},
)
async def delete_account(
    request: UserHttpRequest,
    game_id: Game.GAMES_LITERAL,
    slot_id: int,
) -> None:
    """Удаление слота игры."""
    await AccountsService().unlink(request.auth, game_id, slot_id)


@router.post(
    "/{game_id}/slots/{slot_id}/activate",
    summary="Запуск/остановка работы аккаунта в слоте игры",
    response={200: AccountModelSchema},
)
async def switch_account(
    request: UserHttpRequest,
    game_id: Game.GAMES_LITERAL,
    slot_id: int,
    body: AccountSwitchPlayPostBody,
) -> Any:
    """Запуск/остановка работы аккаунта в слоте игры."""
    return await AccountsService().switch(request.auth, game_id, slot_id, body.play)
