from datetime import UTC, datetime
from typing import cast

from dateutil.relativedelta import relativedelta

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
        game_hash_name: str | None,
    ) -> list[Slot]:
        """
        Получение всех слотов пользователя.

        :param customer_id: идентификатор пользователя
        :param game_hash_name: хэш игры
        :return: список слотов
        """
        return cast(list[Slot], await synct(self.__all)(customer_id, game_hash_name))

    async def add_slot(
        self,
        user_id: int,
        game_hash_name: str,
        payment_hash: str | None,
    ) -> Slot:
        """
        Добавление слота.

        :param user_id: идентификатор пользователя
        :param game_hash_name: хэш игры
        :param payment_hash: хэш платежа
        :return: слот
        """
        return cast(Slot, await synct(self.__add_slot)(user_id, game_hash_name, payment_hash))

    @staticmethod
    @by_transaction
    def __all(customer_id: int, game_hash_name: str) -> list[Slot]:
        """Получение всех слотов пользователя."""
        return list(
            Slot.objects.filter(
                user_id__exact=customer_id,
                game__hash_name__exact=game_hash_name,
            ).select_related("account")
        )

    @staticmethod
    @by_transaction
    def __add_slot(user_id: int, game_hash_name: str, payment_hash: str | None) -> Slot:
        """Добавление слота."""
        return Slot.objects.create(
            user_id=user_id,
            game_id=game_hash_name,
            expired_at=datetime.now(UTC) + relativedelta(hours=1),
        )
