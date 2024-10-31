from ninja import Router

from app.api.v1.billing.router import billing_router
from app.api.v1.game.router import game_router
from app.api.v1.user.router import user_router

v1_router = Router()
v1_router.add_router("/user/", user_router)
v1_router.add_router("/game/", game_router)
v1_router.add_router("/billing/", billing_router)
