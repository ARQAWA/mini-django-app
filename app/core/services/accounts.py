import urllib.parse
from typing import TYPE_CHECKING, Any, cast

from app.core.apps.core.models import Game
from app.core.apps.games.models import Account, Slot
from app.core.apps.stats.dicts.hamster import HamsterStatsSchema
from app.core.apps.stats.models import Play, Network
from app.core.clients.tma_hamster import TMAHamsterKombat
from app.core.common.enums import ErrorsPhrases
from app.core.common.error import ApiError
from app.core.common.executors import get_process_pool, syncp, synct
from app.core.common.fake_ua import fake_user_agent
from app.core.common.initdata import decode_initdata
from app.core.common.singleton import SingletonMeta
from app.core.common.threaded_transaction import by_transaction
from app.core.libs.httpx_ import get_proxy_client
from app.core.services.tokens.hamster import get_raw_init_data

if TYPE_CHECKING:
    from app.api.v1.game.schemas import AccountLinkPutBody


class AccountsService(metaclass=SingletonMeta):
    """Сервис аккаунтов."""

    def __init__(self) -> None:
        self._hamster_client = TMAHamsterKombat()

    async def link(
        self,
        customer_id: int,
        game_id: Game.GAMES_LITERAL,
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
        account = await synct(self.__check_and_get_current_account)(customer_id, game_id, slot_id, body)
        token = await self.__get_token_for_game(game_id, body, agent := fake_user_agent.random, body.proxy)
        return cast(Account, await synct(self.__link)(customer_id, game_id, slot_id, body, token, agent, account))

    async def unlink(
        self,
        customer_id: int,
        game_id: Game.GAMES_LITERAL,
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
        game_id: Game.GAMES_LITERAL,
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

    @by_transaction
    def __check_and_get_current_account(
        self,
        customer_id: int,
        game_id: Game.GAMES_LITERAL,
        slot_id: int,
        body: "AccountLinkPutBody",
    ) -> Account | None:
        """Проверка текущего аккаунта в слоте игры."""
        slot: Slot | None = (
            Slot.objects.select_related("account").filter(id=slot_id, customer_id=customer_id, game_id=game_id).first()
        )

        if slot is None:
            raise ApiError.failed_dependency(ErrorsPhrases.SLOT_NOT_FOUND)

        if slot.account_id is None:
            return None

        decoded_initdata: dict[str, str] = get_process_pool().submit(decode_initdata, body.init_data).result()
        tg_id_from_initdata = decoded_initdata["user"].split('"id":')[1].split(",")[0].split("}")[0]

        account_sign = urllib.parse.quote(urllib.parse.quote(f'"id":{tg_id_from_initdata},'))

        account = cast(Account, slot.account)
        if account_sign not in account.init_data:
            raise ApiError.conflict(ErrorsPhrases.INITDATA_FROM_OTHER_ACCOUNT)

        return account

    @by_transaction
    def __link(
        self,
        customer_id: int,
        game_id: Game.GAMES_LITERAL,
        slot_id: int,
        body: "AccountLinkPutBody",
        auth_token: str,
        user_agent: str,
        account: Account | None,
    ) -> Account:
        """Привязка аккаунта к слоту."""
        if account is not None:
            account.init_data = body.init_data
            account.proxy_url = body.proxy
            account.save()
            return Account.objects.select_related("play", "network").get(id=account.id)

        account = Account.objects.create(
            tg_id=body.tg_id,
            customer_id=customer_id,
            game_id=game_id,
            first_name=body.first_name,
            last_name=body.last_name,
            username=body.username,
            init_data=body.init_data,
            proxy_url=body.proxy,
            auth_token=auth_token,
            user_agent=user_agent,
        )

        Slot.objects.filter(id=slot_id).update(account=account)
        Play.objects.create(account=account, stats_dict=self.__create_stats_by_game(game_id))
        Network.objects.create(account=account)

        return Account.objects.select_related("play", "network").get(id=account.id)

    @staticmethod
    @by_transaction
    def __unlink(
        customer_id: int,
        game_id: Game.GAMES_LITERAL,
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
        game_id: Game.GAMES_LITERAL,
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

    @by_transaction
    def __reset(self, customer_id: int, game_id: Game.GAMES_LITERAL, slot_id: int) -> Account:
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

        self.__reset_stats_by_game(game_id, account)
        account.network.reset()

        return account

    @staticmethod
    def __create_stats_by_game(game_id: Game.GAMES_LITERAL) -> dict[str, Any]:
        """Создание статистики аккаунта в слоте игры."""
        match game_id:
            case Game.LITERAL_HAMSTER_KOMBAT:
                return cast(dict[str, Any], HamsterStatsSchema.get_hamster_dict())
            case _:
                raise ApiError.bad_request(ErrorsPhrases.GAME_NOT_FOUND)

    @staticmethod
    def __reset_stats_by_game(game_id: Game.GAMES_LITERAL, account: Account) -> None:
        """Сброс статистики аккаунта в слоте игры."""
        match game_id:
            case Game.LITERAL_HAMSTER_KOMBAT:
                reseted_stats = HamsterStatsSchema.get_hamster_dict()
            case _:
                raise ApiError.bad_request(ErrorsPhrases.GAME_NOT_FOUND)

        account.play.stats_dict = reseted_stats
        account.play.save()

    async def __get_token_for_game(
        self,
        game_id: Game.GAMES_LITERAL,
        body: "AccountLinkPutBody",
        agent: str,
        proxy_url: str | None,
    ) -> str:
        """Получение токена для игры."""
        proxy_client = None if proxy_url is None else get_proxy_client(proxy_url)
        match game_id:
            case Game.LITERAL_HAMSTER_KOMBAT:
                raw_init_data = await syncp(get_raw_init_data)(body.init_data)
                return await self._hamster_client.auth_tg_webapp(raw_init_data, agent, proxy_client)
            case _:
                raise ApiError.bad_request(ErrorsPhrases.GAME_NOT_FOUND)
