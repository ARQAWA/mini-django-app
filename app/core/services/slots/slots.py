from typing import cast

from app.core.apps.games.models import Slot
from app.core.clients.redis_ import redis_client
from app.core.common.executors import synct
from app.core.common.singleton import SingletonMeta
from app.core.common.threaded_transaction import by_transaction
from app.core.repositories.web_auth import WebAuthRepo


class SlotsService(metaclass=SingletonMeta):
    """Сервис слотов."""

    def __init__(self) -> None:
        self._redis_client = redis_client
        self._web_auth_repo = WebAuthRepo()

    async def all(
        self,
        customer_id: int,
        game_hash_name: str,
    ) -> list[Slot]:
        """
        Получение всех слотов пользователя.

        :param customer_id: идентификатор пользователя
        :param game_hash_name: хэш игры
        :return: список слотов
        """
        return cast(list[Slot], await synct(self.__all)(customer_id, game_hash_name))

    # @staticmethod
    # @by_transaction
    # def __auth_user(user_str: bytes, refresh: bytes) -> Customer:
    #     """
    #     Обновление пользователя.
    #
    #     :param user_str: данные пользователя
    #     :param refresh: refresh токен
    #     :return: пользователь
    #     """
    #     user_obj: UserData.Dict = orjson.loads(user_str)
    #     user: Customer
    #     user, _ = Customer.objects.get_or_create(  # noqa: F841
    #         id=user_obj["id"],
    #         defaults=dict(
    #             first_name=user_obj["first_name"],
    #             last_name=user_obj["last_name"],
    #             username=user_obj["username"],
    #             refresh_token="__temp__",
    #         ),
    #     )
    #     user.refresh_token = refresh.decode()
    #     user.save()
    #     return user
    #
    # @staticmethod
    # @by_transaction
    # def __update_refresh_token(refresh_old: bytes, refresh_new: bytes) -> Customer | None:
    #     """
    #     Обновление пользователя.
    #
    #     :param refresh_old: старый refresh токен
    #     :param refresh_new: новый refresh токен
    #     :return: пользователь
    #     """
    #     user: Customer
    #     try:
    #         user = Customer.objects.get(refresh_token=refresh_old.decode())
    #         user.refresh_token = refresh_new.decode()
    #         user.save()
    #         return user
    #     except Customer.DoesNotExist:
    #         return None
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
