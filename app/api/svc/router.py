from ninja import Router

from app.api.svc.router_billing import billing_router
from app.api.svc.router_game import slots_router
from app.core.common.ninjas_fix.auth_dep import BrosSecretAuthDepends

svc_router = Router(auth=BrosSecretAuthDepends())
svc_router.add_router("/billing/", billing_router)
svc_router.add_router("/game/", slots_router)
