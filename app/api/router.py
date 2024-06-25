from app.api.v1.router import router as v1_router
from app.core.common.ninjas_fix.auth_dep import UserAuthDepends
from app.core.common.ninjas_fix.router import Router

router = Router(auth=UserAuthDepends())
router.add_router("/v1/", v1_router)
