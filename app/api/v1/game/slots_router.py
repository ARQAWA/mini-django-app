from typing import Any

from app.core.apps.core.models import Game
from app.core.apps.games.schemas import SlotModelSchema
from app.core.common.ninjas_fix.auth_dep import UserHttpRequest
from app.core.common.ninjas_fix.router import Router
from app.core.services.slots.slots import SlotsService

router = Router(tags=["slots"])


@router.get(
    "/{game_hash_name}/slots",
    summary="Получение слотов игры",
    response={200: list[SlotModelSchema]},
)
async def get_slots(request: UserHttpRequest, game_hash_name: Game.GAMES_LITERAL) -> Any:
    """Получение слотов игры."""
    result = await SlotsService().all(request.auth.id, game_hash_name)
    return result


# @router.post(
#     "/{game_hash_name}/slots",
#     summary="Добавление слота игры",
#     response={200: dict},
# )
# async def add_slot(request: UserHttpRequest) -> DictStrAny:
#     """Добавление слота игры."""
#     return {"game_hash_name": request.path_params["game_hash_name"]}
