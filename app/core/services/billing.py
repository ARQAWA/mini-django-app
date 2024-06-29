import asyncio
import time
from datetime import timedelta
from typing import Any, cast

from django.db.models import Case, DecimalField, Sum, Value, When
from django.db.models.functions import Now

from app.core.apps.core.models import Payment
from app.core.apps.games.models import Slot
from app.core.clients.ton_api import TonApiClient
from app.core.common.executors import synct
from app.core.common.singleton import SingletonMeta
from app.core.common.threaded_transaction import by_transaction


class BillingService(metaclass=SingletonMeta):
    """Сервис слотов."""

    def __init__(self) -> None:
        self.__lock = asyncio.Lock()
        self.__last_checked = time.time()

        self._ton_client = TonApiClient()

    async def check_payment(self) -> None:
        """Проверка платежей."""
        async with self.__lock:
            if (cur := time.time()) - self.__last_checked < 5:
                return

            self.__last_checked = cur
            payed_data = await self._ton_client.get_payed_list()

            if not payed_data:
                return

            await synct(self.__apply_payments)(payed_data)

    async def stats(self) -> dict[str, int]:
        """Статистика."""
        return cast(dict[str, int], await synct(self.__stats)())

    @staticmethod
    @by_transaction
    def __apply_payments(payed_data: list[tuple[str, int]]) -> None:
        """Проведение платежей."""
        non_payed_ids = set(Payment.objects.select_for_update().filter(is_payed=False).values_list("id", flat=True))
        tuple(Slot.objects.select_for_update().filter(payment_id__in=non_payed_ids).values_list("id", flat=True))

        ids, cases = [], []
        for pid, value in payed_data:
            if pid in non_payed_ids:
                ids.append(pid)
                cases.append(When(id=pid, then=Value(value)))

        if ids:
            Slot.objects.filter(payment__id__in=ids).update(expired_at=Now() + timedelta(days=31))
            Payment.objects.filter(id__in=ids).update(amount=Case(*cases, output_field=DecimalField()), is_payed=True)

    @staticmethod
    @by_transaction
    def __stats() -> dict[str, Any]:
        """Статистика."""
        ton = Payment.Type.TON.value

        payments_count = Payment.objects.filter(type=ton).count() or 0
        payments_amount = Payment.objects.filter(type=ton).aggregate(amount_sum=Sum("amount"))["amount_sum"] or 0
        payed_count = Payment.objects.filter(type=ton, is_payed=True).count() or 0
        payed_amount = (
            Payment.objects.filter(type=ton, is_payed=True).aggregate(amount_sum=Sum("amount"))["amount_sum"] or 0
        )

        today_count = Payment.objects.filter(type=ton, created_at__date=Now()).count() or 0
        today_amount = (
            (Payment.objects.filter(type=ton, created_at__date=Now()).aggregate(amount_sum=Sum("amount"))["amount_sum"])
            or 0
        )
        today_payed_count = Payment.objects.filter(type=ton, is_payed=True, created_at__date=Now()).count() or 0
        today_payed_amount = (
            (
                Payment.objects.filter(type=ton, is_payed=True, created_at__date=Now()).aggregate(
                    amount_sum=Sum("amount")
                )["amount_sum"]
            )
            or 0
        )

        return {
            "payments_count": f"{payed_count}/{payments_count} | diff: +{payments_count - payed_count}",
            "payments_amount": f"{payed_amount}/{payments_amount} | diff: +{payments_amount - payed_amount}",
            "today": {
                "count": f"{today_payed_count}/{today_count} | diff: +{today_count - today_payed_count}",
                "amount": f"{today_payed_amount}/{today_amount} | diff: +{today_amount - today_payed_amount}",
            },
        }
