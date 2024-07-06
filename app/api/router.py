from ninja import Router

from app.api.svc.router import svc_router
from app.api.v1.router import v1_router
from app.core.common.ninjas_fix.auth_dep import UserAuthDepends

router = Router(auth=UserAuthDepends())
router.add_router("/v1/", v1_router)

router.add_router("/svc/", svc_router)
