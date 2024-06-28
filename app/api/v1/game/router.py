from app.api.v1.game.router_slots import router as slots_router
from app.core.common.ninjas_fix.router import Router

router = Router()
router.add_router("", slots_router)
