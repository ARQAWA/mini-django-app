from ninja import Router
from ninja.types import DictStrAny

from app.core.common.ninjas_fix.auth_dep import UserHttpRequest
from app.core.services.billing import BillingService

billing_router = Router()


@billing_router.get(
    "/stats",
    summary="Статистика",
    response={200: DictStrAny},
)
async def stats(request: UserHttpRequest) -> DictStrAny:
    """Статистика."""
    return await BillingService().stats()
