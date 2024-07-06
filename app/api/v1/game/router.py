from ninja import Router

from app.api.v1.game.router_accounts import accounts_router
from app.api.v1.game.router_slots import slots_router

game_router = Router()
game_router.add_router("", slots_router)
game_router.add_router("", accounts_router)
