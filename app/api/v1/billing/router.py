from ninja.types import DictStrAny

from app.core.common.ninjas_fix.auth_dep import BrosSecretAuthDepends, UserHttpRequest
from app.core.common.ninjas_fix.router import Router
from app.core.services.billing import BillingService

router = Router(tags=["billing"])


@router.get(
    "/stats",
    summary="Статистика",
    response={200: DictStrAny},
    auth=BrosSecretAuthDepends(),
)
async def stats(request: UserHttpRequest) -> DictStrAny:
    """Статистика."""
    return await BillingService().stats()


@router.get(
    "/check_payment",
    summary="Проверка платежа",
    response={200: None},
)
async def check_payment(request: UserHttpRequest) -> None:
    """Проверка платежа."""
    await BillingService().check_payment()
