from app.api.v1.billing.router import router as billing_router
from app.api.v1.game.router import router as game_router
from app.api.v1.user.router import router as user_router
from app.core.common.ninjas_fix.router import Router

router = Router()
router.add_router("/user/", user_router)
router.add_router("/game/", game_router)
router.add_router("/billing/", billing_router)
