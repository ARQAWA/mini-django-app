from typing import TYPE_CHECKING, cast

from app.core.apps.core.models import Payment
from app.core.apps.games.models import Slot
from app.core.common.db_date import demo_expired
from app.core.common.error import ApiError
from app.core.common.executors import synct
from app.core.common.gen_random_string import sync_get_rand_string
from app.core.common.singleton import SingletonMeta
from app.core.common.threaded_transaction import by_transaction
from app.core.repositories.web_auth import WebAuthRepo

if TYPE_CHECKING:
    from app.api.v1.game.schemas import SlotCreatePostBody


class SlotsService(metaclass=SingletonMeta):
    """Сервис слотов."""

    def __init__(self) -> None:
        self._web_auth_repo = WebAuthRepo()

    async def all(
        self,
        customer_id: int,
        game_id: str | None,
    ) -> list[Slot]:
        """
        Получение всех слотов пользователя.

        :param customer_id: идентификатор пользователя
        :param game_id: хэш игры
        :return: список слотов
        """
        return cast(list[Slot], await synct(self.__all)(customer_id, game_id))

    async def add_slot(self, customer_id: int, game_id: str, body: "SlotCreatePostBody") -> Slot:
        """
        Добавление слота.

        :param customer_id: идентификатор пользователя
        :param game_id: хэш игры
        :param body: тело запроса
        :return: слот
        """
        return cast(Slot, await synct(self.__add_slot)(customer_id, game_id, body))

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
                raise ApiError.not_acceptable("Demo slot creation is not allowed")
            payment_id = sync_get_rand_string(64).decode()
            payment = Payment.objects.create(id=payment_id, amount=0, is_payed=True, type=Payment.Type.DEMO.value)
            return Slot.objects.create(customer_id=cid, game_id=gid, payment=payment, expired_at=demo_expired())
        return Slot.objects.create(customer_id=cid, game_id=gid)
