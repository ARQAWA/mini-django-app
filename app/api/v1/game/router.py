from app.api.v1.game.router_accounts import router as accounts_router
from app.api.v1.game.router_slots import router as slots_router
from app.core.common.ninjas_fix.router import Router

router = Router()
router.add_router("", slots_router)
router.add_router("", accounts_router)
