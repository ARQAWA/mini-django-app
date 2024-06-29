from app.core.apps.core.models import Payment
from app.core.clients.ton_api import TonApiClient
from app.core.common.singleton import SingletonMeta


class BillingService(metaclass=SingletonMeta):
    """Сервис слотов."""

    def __init__(self) -> None:
        self._ton_client = TonApiClient()

    async def check_payment(self) -> None:
        """Проверка платежей."""
        payed_ids = await self._ton_client.get_payed_list()

        if payed_ids:
            await Payment.objects.filter(id__in=payed_ids, is_payed=False).aupdate(is_payed=True)
