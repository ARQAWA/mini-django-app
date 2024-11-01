from datetime import UTC, datetime
from typing import TYPE_CHECKING, cast

from app.core.apps.core.models import Payment
from app.core.apps.games.models import Account, Slot
from app.core.common.db_date import demo_expired, utc_now_plus_month
from app.core.common.enums import ErrorsPhrases
from app.core.common.error import ApiError
from app.core.common.executors import synct
from app.core.common.gen_random_string import sync_get_rand_string
from app.core.common.singleton import SingletonMeta
from app.core.common.threaded_transaction import by_transaction
from app.core.repositories.web_auth import WebAuthRepo
from app.core.services.billing import BillingService

if TYPE_CHECKING:
    from app.api.v1.game.schemas import SlotCreatePostBody


class SlotsService(metaclass=SingletonMeta):
    """Сервис слотов."""

    def __init__(self) -> None:
        self._web_auth_repo = WebAuthRepo()
        self._billing_service = BillingService()

    async def all(
        self,
        customer_id: int,
        game_id: str | None,
    ) -> list[Slot]:
        """
        Получение всех слотов пользователя.

        :param customer_id: идентификатор пользователя
        :param game_id: идентификатор игры
        :return: список слотов
        """
        return cast(list[Slot], await synct(self.__all)(customer_id, game_id))

    async def add_slot(self, customer_id: int, game_id: str, body: "SlotCreatePostBody") -> Slot:
        """
        Добавление слота.

        :param customer_id: идентификатор пользователя
        :param game_id: идентификатор игры
        :param body: тело запроса
        :return: слот
        """
        return cast(Slot, await synct(self.__add_slot)(customer_id, game_id, body))

    async def delete_slot(self, customer_id: int, game_id: str, slot_id: int) -> None:
        """
        Удаление слота.

        :param customer_id: идентификатор пользователя
        :param game_id: идентификатор игры
        :param slot_id: идентификатор слота.
        """
        await synct(self.__delete_slot)(customer_id, game_id, slot_id)

    @staticmethod
    @by_transaction
    def __all(customer_id: int, game_id: str) -> list[Slot]:
        """Получение всех слотов пользователя."""
        return list(
            Slot.objects.filter(
                customer_id=customer_id,
                game_id=game_id,
            ).select_related("account", "account__play", "account__network", "payment")
        )

    @staticmethod
    @by_transaction
    def __add_slot(cid: int, gid: str, body: "SlotCreatePostBody") -> Slot:
        """Добавление слота."""
        if body.is_demo:
            if Slot.objects.select_for_update().filter(customer_id=cid, game_id=gid).exists():
                raise ApiError.not_acceptable(ErrorsPhrases.DEMO_SLOT_NOT_AVAILABLE)

            payment_id = sync_get_rand_string(64).decode()
            payment = Payment.objects.create(id=payment_id, amount=0, is_payed=True, type=Payment.Type.DEMO.value)

            return Slot.objects.create(customer_id=cid, game_id=gid, payment=payment, expired_at=demo_expired())

        payment_id = cast(str, body.payment_hash)
        payment = Payment.objects.create(id=payment_id, amount=0, is_payed=False, type=Payment.Type.TON.value)

        if body.slot_id is not None:
            slot: Slot | None = (
                Slot.objects.select_for_update()
                .select_related("payment")
                .filter(id=body.slot_id, customer_id=cid, game_id=gid)
                .first()
            )
            if slot is None:
                raise ApiError.failed_dependency(ErrorsPhrases.SLOT_NOT_FOUND)

            if not slot.payment.is_payed or slot.expired_at > datetime.now(UTC):
                raise ApiError.not_acceptable(ErrorsPhrases.PAYMENT_EXTENSION_NOT_ALLOWED)

            slot.payment = payment
            slot.expired_at = utc_now_plus_month()

            slot.save()
            return slot

        return Slot.objects.create(customer_id=cid, game_id=gid, payment=payment, expired_at=utc_now_plus_month())

    @staticmethod
    @by_transaction
    def __get_checked_slot(cid: int, gid: str, sid: int) -> Slot:
        """Получение слота с проверкой."""
        slot: Slot | None = Slot.objects.filter(id=sid, customer_id=cid, game_id=gid).first()

        if slot is None:
            raise ApiError.failed_dependency(ErrorsPhrases.SLOT_NOT_FOUND)

        return slot

    @staticmethod
    @by_transaction
    def __delete_slot(cid: int, gid: str, sid: int) -> None:
        """Удаление слота."""
        slot: Slot | None
        slot = Slot.objects.filter(id=sid, customer_id=cid, game_id=gid).only("id", "account_id", "payment_id").first()
        if slot is None:
            raise ApiError.failed_dependency(ErrorsPhrases.SLOT_NOT_FOUND)
        pid, aid = slot.payment_id, slot.account_id

        slot.delete()
        Payment.objects.filter(id=pid).delete()
        if aid is not None:
            Account.objects.filter(id=aid).delete()
