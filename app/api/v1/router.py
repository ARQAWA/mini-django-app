from app.api.v1.user.router import router as user_router
from app.core.common.ninjas_fix.router import Router

router = Router()
router.add_router("/user/", user_router)
