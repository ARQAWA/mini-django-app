from ninja import Router

from app.core.apps.core.models import Game
from app.core.common.ninjas_fix.auth_dep import UserHttpRequest
from app.core.services.slots import SlotsService

slots_router = Router()


@slots_router.delete(
    "/{game_id}/service_route/slots/{slot_id}",
    summary="Удаление слота игры",
    response={200: None},
)
async def delete_slot(
    request: UserHttpRequest,
    game_id: Game.GAMES_LITERAL,
    slot_id: int,
) -> None:
    """Удаление слота игры."""
    await SlotsService().delete_slot(request.auth, game_id, slot_id)
