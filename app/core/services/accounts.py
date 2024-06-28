import contextlib
from datetime import UTC, datetime
from enum import StrEnum
from typing import cast

from app.core.apps.games.models import Account, Slot
from app.core.common.error import ApiError
from app.core.common.executors import synct
from app.core.common.singleton import SingletonMeta
from app.core.common.threaded_transaction import by_transaction


class ErrorsPhrases(StrEnum):
    """Строки ошибок."""

    SLOT_NOT_FOUND = "SLOT_NOT_FOUND"  # слот не найден
    ANOTHER_USER_LINKED = "ANOTHER_USER_LINKED"  # аккаунт уже привязан к другому пользователю
    ANOTHER_SLOT_LINKED = "ANOTHER_SLOT_LINKED"  # аккаунт уже привязан к другому слоту


class AccountsService(metaclass=SingletonMeta):
    """Сервис аккаунтов."""

    async def link(
        self,
        customer_id: int,
        game_hash_name: str,
        slot_id: int,
        init_data: str,
        proxy: str | None,
    ) -> Account:
        """
        Привязка аккаунта к слоту.

        :param customer_id: идентификатор пользователя
        :param game_hash_name: хэш игры
        :param slot_id: идентификатор слота
        :param init_data: данные инициализации
        :param proxy: прокси
        :return: хэш аккаунта
        """
        return cast(Account, await synct(self.__link)(customer_id, game_hash_name, slot_id, init_data, proxy))

    async def unlink(self, customer_id: int, game_hash_name: str, slot_id: int) -> None:
        """
        Отвязка аккаунта от слота.

        :param customer_id: идентификатор пользователя
        :param game_hash_name: хэш игры
        :param slot_id: идентификатор слота
        """
        await synct(self.__unlink)(customer_id, game_hash_name, slot_id)

    @staticmethod
    @by_transaction
    def __link(
        customer_id: int,
        game_hash_name: str,
        slot_id: int,
        init_data: str,
        proxy: str | None,
    ) -> Account:
        """Привязка аккаунта к слоту."""
        account, _ = Account.objects.update_or_create(  # noqa: F841
            tg_id=12345,
            customer_id=customer_id,
            game_id=game_hash_name,
            defaults=dict(
                first_name="First Name",
                last_name="Last Name",
                username="Username",
                init_data=init_data,
                proxy_url=proxy,
            ),
        )

        try:
            slot = Slot.objects.select_related("account").get(
                id=slot_id,
                customer_id=customer_id,
                game_id=game_hash_name,
            )
        except Slot.DoesNotExist:
            raise ApiError.failed_dependency(ErrorsPhrases.SLOT_NOT_FOUND)

        # noinspection PyTypeChecker
        with contextlib.suppress(Slot.DoesNotExist):
            another_slot = Slot.objects.exclude(id=slot_id).get(
                customer_id=customer_id,
                game_id=game_hash_name,
                account_id=account.id,
            )
            if another_slot.expired_at <= datetime.now(UTC):
                another_slot.delete()
            else:
                another_slot.account = None
                another_slot.save()

        slot.account = account
        slot.save()

        return account

    @staticmethod
    @by_transaction
    def __unlink(
        customer_id: int,
        game_hash_name: str,
        slot_id: int,
    ) -> None:
        """Отвязка аккаунта от слота."""
        try:
            slot = Slot.objects.get(
                id=slot_id,
                customer_id=customer_id,
                game_id=game_hash_name,
            )
            if slot.account is not None:
                slot.account = None
                slot.save()
        except Slot.DoesNotExist:
            raise ApiError.failed_dependency(ErrorsPhrases.SLOT_NOT_FOUND)
