import contextlib
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

    @staticmethod
    @by_transaction
    def __link(
        customer_id: int,
        game_id: str,
        slot_id: int,
        body: "AccountLinkPutBody",
    ) -> Account:
        """Привязка аккаунта к слоту."""
        account, is_created = Account.objects.update_or_create(  # noqa: F841
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

        try:
            slot = Slot.objects.select_related("account").get(id=slot_id, customer_id=customer_id, game_id=game_id)
        except Slot.DoesNotExist:
            raise ApiError.failed_dependency(ErrorsPhrases.SLOT_NOT_FOUND)

        # noinspection PyTypeChecker
        with contextlib.suppress(Slot.DoesNotExist):
            another_slot = Slot.objects.exclude(id=slot_id).get(account_id=account.id)
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
