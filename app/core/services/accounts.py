from enum import StrEnum
from typing import TYPE_CHECKING, cast

from app.core.apps.games.models import Account, Slot
from app.core.apps.stats.models import Network as NetworkStats
from app.core.apps.stats.models import Play as PlayStats
from app.core.common.error import ApiError
from app.core.common.executors import synct
from app.core.common.singleton import SingletonMeta
from app.core.common.threaded_transaction import by_transaction

if TYPE_CHECKING:
    from app.api.v1.game.schemas import AccountLinkPutBody


class ErrorsPhrases(StrEnum):
    """Строки ошибок."""

    SLOT_NOT_FOUND = "SLOT_NOT_FOUND"  # слот не найден
    ACCOUNT_NOT_FOUND = "ACCOUNT_NOT_FOUND"  # аккаунт не найден
    ANOTHER_USER_LINKED = "ANOTHER_USER_LINKED"  # аккаунт уже привязан к другому пользователю
    ANOTHER_SLOT_LINKED = "ANOTHER_SLOT_LINKED"  # аккаунт уже привязан к другому слоту


class AccountsService(metaclass=SingletonMeta):
    """Сервис аккаунтов."""

    async def link(
        self,
        customer_id: int,
        game_id: str,
        slot_id: int,
        body: "AccountLinkPutBody",
    ) -> Account:
        """
        Привязка аккаунта к слоту.

        :param customer_id: идентификатор пользователя
        :param game_id: идентификатор игры
        :param slot_id: идентификатор слота
        :param body: данные аккаунта
        :return: аккаунт
        """
        return cast(Account, await synct(self.__link)(customer_id, game_id, slot_id, body))

    async def unlink(
        self,
        customer_id: int,
        game_id: str,
        slot_id: int,
    ) -> None:
        """
        Отвязка аккаунта от слота.

        :param customer_id: идентификатор пользователя
        :param game_id: идентификатор игры
        :param slot_id: идентификатор слота
        """
        await synct(self.__unlink)(customer_id, game_id, slot_id)

    async def switch(
        self,
        customer_id: int,
        game_id: str,
        slot_id: int,
        play: bool,
    ) -> Account:
        """
        Запуск/остановка работы аккаунта в слоте игры.

        :param customer_id: идентификатор пользователя
        :param game_id: идентификатор игры
        :param slot_id: идентификатор слота
        :param play: флаг работы аккаунта
        """
        return cast(Account, await synct(self.__switch)(customer_id, game_id, slot_id, play))

    async def reset(self, customer_id: int, game_id: str, slot_id: int) -> Account:
        """
        Сброс статистики аккаунта в слоте игры.

        :param customer_id: идентификатор пользователя
        :param game_id: идентификатор игры
        :param slot_id: идентификатор слота
        :return: аккаунт.
        """
        return cast(Account, await synct(self.__reset)(customer_id, game_id, slot_id))

    @staticmethod
    @by_transaction
    def __link(
        customer_id: int,
        game_id: str,
        slot_id: int,
        body: "AccountLinkPutBody",
    ) -> Account:
        """Привязка аккаунта к слоту."""
        account, is_created = Account.objects.update_or_create(
            tg_id=body.tg_id,
            customer_id=customer_id,
            game_id=game_id,
            defaults=dict(
                first_name=body.first_name,
                last_name=body.last_name,
                username=body.username,
                init_data=body.init_data,
                proxy_url=body.proxy,
            ),
        )

        if is_created:
            PlayStats.objects.create(account=account)
            NetworkStats.objects.create(account=account)

        slot: Slot | None = Slot.objects.filter(id=slot_id, customer_id=customer_id, game_id=game_id).first()

        if slot is None:
            raise ApiError.failed_dependency(ErrorsPhrases.SLOT_NOT_FOUND)

        another_slot: Slot | None = Slot.objects.exclude(id=account.id).filter(account_id=account.id).first()
        if another_slot is not None:
            another_slot.account = None
            another_slot.save()

        slot.account = account
        slot.save()

        return Account.objects.select_related("play", "network").get(id=account.id)

    @staticmethod
    @by_transaction
    def __unlink(
        customer_id: int,
        game_id: str,
        slot_id: int,
    ) -> None:
        """Отвязка аккаунта от слота."""
        slot: Slot | None = Slot.objects.filter(id=slot_id, customer_id=customer_id, game_id=game_id).first()

        if slot is None:
            raise ApiError.failed_dependency(ErrorsPhrases.SLOT_NOT_FOUND)

        if slot.account is not None:
            slot.account = None
            slot.save()

    @staticmethod
    @by_transaction
    def __switch(
        customer_id: int,
        game_id: str,
        slot_id: int,
        play: bool,
    ) -> Account:
        """Запуск/остановка работы аккаунта в слоте игры."""
        account: Account | None = (
            Account.objects.filter(
                slot=slot_id,
                customer_id=customer_id,
                game_id=game_id,
            )
            .select_related("play", "network")
            .first()
        )

        if account is None:
            raise ApiError.failed_dependency(ErrorsPhrases.ACCOUNT_NOT_FOUND)

        if account.is_playing != play:
            account.is_playing = play
            account.save()

        return account

    @staticmethod
    @by_transaction
    def __reset(customer_id: int, game_id: str, slot_id: int) -> Account:
        """Сброс статистики аккаунта в слоте игры."""
        account: Account | None = (
            Account.objects.filter(
                slot=slot_id,
                customer_id=customer_id,
                game_id=game_id,
            )
            .select_related("play", "network")
            .first()
        )

        if account is None:
            raise ApiError.failed_dependency(ErrorsPhrases.ACCOUNT_NOT_FOUND)

        account.play.reset()
        account.network.reset()

        return account
