from typing import cast

from app.core.apps.games.models import Slot
from app.core.common.executors import synct
from app.core.common.singleton import SingletonMeta
from app.core.common.threaded_transaction import by_transaction
from app.core.repositories.web_auth import WebAuthRepo


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

    async def add_slot(
        self,
        customer_id: int,
        game_id: str,
        payment_hash: str | None,
    ) -> Slot:
        """
        Добавление слота.

        :param customer_id: идентификатор пользователя
        :param game_id: хэш игры
        :param payment_hash: хэш платежа
        :return: слот
        """
        return cast(Slot, await synct(self.__add_slot)(customer_id, game_id, payment_hash))

    @staticmethod
    @by_transaction
    def __all(customer_id: int, game_id: str) -> list[Slot]:
        """Получение всех слотов пользователя."""
        return list(
            Slot.objects.filter(
                customer_id=customer_id,
                game_id=game_id,
            ).select_related("account", "account__play", "account__network")
        )

    @staticmethod
    @by_transaction
    def __add_slot(customer_id: int, game_id: str, payment_hash: str | None) -> Slot:
        """Добавление слота."""
        return Slot.objects.create(
            customer_id=customer_id,
            game_id=game_id,
        )
