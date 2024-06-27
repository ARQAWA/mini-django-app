from app.core.common.singleton import SingletonMeta


class AccountsService(metaclass=SingletonMeta):
    """Сервис аккаунтов."""

    async def link(
        self,
        customer_id: int,
        game_hash_name: str,
        slot_id: int,
        init_data: str,
        proxy: str | None,
    ) -> str:
        """
        Привязка аккаунта к слоту.

        :param customer_id: идентификатор пользователя
        :param game_hash_name: хэш игры
        :param slot_id: идентификатор слота
        :param init_data: данные инициализации
        :param proxy: прокси
        :return: хэш аккаунта
        """
        return ""

    # async def all(
    #     self,
    #     customer_id: int,
    #     game_hash_name: str,
    # ) -> list[Slot]:
    #     """
    #     Получение всех слотов пользователя.
    #
    #     :param customer_id: идентификатор пользователя
    #     :param game_hash_name: хэш игры
    #     :return: список слотов
    #     """
    #     return cast(list[Slot], await synct(self.__all)(customer_id, game_hash_name))
    #
    # async def add_slot(self, user_id: int, game_hash_name: str) -> Slot:
    #     """
    #     Добавление слота.
    #
    #     :param user_id: идентификатор пользователя
    #     :param game_hash_name: хэш игры
    #     :return: слот
    #     """
    #     return cast(Slot, await synct(self.__add_slot)(user_id, game_hash_name))
    #
    # @staticmethod
    # @by_transaction
    # def __all(customer_id: int, game_hash_name: str) -> list[Slot]:
    #     """Получение всех слотов пользователя."""
    #     return list(
    #         Slot.objects.filter(
    #             user_id__exact=customer_id,
    #             game__hash_name__exact=game_hash_name,
    #         ).select_related("account")
    #     )
    #
    # @staticmethod
    # @by_transaction
    # def __add_slot(user_id: int, game_hash_name: str) -> Slot:
    #     """Добавление слота."""
    #     return Slot.objects.create(
    #         user_id=user_id, game_id=game_hash_name, expired_at=datetime.now(UTC) + relativedelta(hours=1)
    #     )
