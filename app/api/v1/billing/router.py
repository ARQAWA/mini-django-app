from ninja import Router

from app.core.common.ninjas_fix.auth_dep import UserHttpRequest
from app.core.services.billing import BillingService

billing_router = Router(tags=["billing"])


@billing_router.get(
    "/check_payment",
    summary="Проверка платежа",
    response={200: None},
)
async def check_payment(request: UserHttpRequest) -> None:
    """Проверка платежа."""
    await BillingService().check_payment()
