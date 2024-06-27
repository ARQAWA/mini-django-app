from ninja.types import DictStrAny

from app.core.common.ninjas_fix.auth_dep import UserHttpRequest
from app.core.common.ninjas_fix.router import Router

router = Router(tags=["slots"])


@router.get(
    "/{game_hash_name}/slots",
    summary="Получение слотов игры",
    response={200: dict},
)
async def get_slots(request: UserHttpRequest) -> DictStrAny:
    """Получение слотов игры."""
    return {"game_hash_name": request.path_params["game_hash_name"]}


@router.post(
    "/{game_hash_name}/slots",
    summary="Добавление слота игры",
    response={200: dict},
)
async def add_slot(request: UserHttpRequest) -> DictStrAny:
    """Добавление слота игры."""
    return {"game_hash_name": request.path_params["game_hash_name"]}
