from typing import Any

from ninja import Router

from app.api.v1.game.schemas import AccountLinkPutBody, AccountSwitchPlayPostBody
from app.core.apps.core.models import Game
from app.core.apps.games.schemas import AccountModelSchema
from app.core.common.ninjas_fix.auth_dep import UserHttpRequest
from app.core.services.accounts import AccountsService

accounts_router = Router(tags=["accounts"])


@accounts_router.put(
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


@accounts_router.delete(
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


@accounts_router.patch(
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


@accounts_router.patch(
    "/{game_id}/slots/{slot_id}/reset",
    summary="Сброс статистики аккаунта в слоте игры",
    response={200: AccountModelSchema},
)
async def reset_account(
    request: UserHttpRequest,
    game_id: Game.GAMES_LITERAL,
    slot_id: int,
) -> Any:
    """Сброс статистики аккаунта в слоте игры."""
    return await AccountsService().reset(request.auth, game_id, slot_id)
