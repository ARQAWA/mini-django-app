import time
from typing import cast

import orjson
from httpx import AsyncClient

from app.core.common.enums import ErrorsPhrases
from app.core.common.error import ApiError
from app.core.common.executors import synct
from app.core.common.singleton import SingletonMeta
from app.core.libs.httpx_ import httpx_client
from app.tap_robotics.hamster_kombat.dicts.clicker_tasks import ClickerTaskDict
from app.tap_robotics.hamster_kombat.dicts.clicker_upgrade import ClickerDailyComboDict, ClickerUpgradeDict
from app.tap_robotics.hamster_kombat.dicts.clicker_user import ClickerUserDict


class TMAHamsterKombat(metaclass=SingletonMeta):
    """Клиент для работы с TMA Hamster Kombat."""

    _base_core = "https://api.hamsterkombatgame.io"
    _base_url = f"{_base_core}/clicker"

    def __init__(self) -> None:
        self._httpx_client = httpx_client

    @staticmethod
    def __get_headers(token: str | None, user_agent: str) -> dict[str, str]:
        """Получить заголовки для запроса к TMA Hamster Kombat."""
        return {
            "User-Agent": user_agent,
            "Authorization": ("Bearer " + token) if token is not None else "",
            "Origin": "https://hamsterkombatgame.io",
            "Referer": "https://hamsterkombatgame.io/",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
        }

    async def auth_tg_webapp(
        self,
        raw_initdata: str,
        user_agent: str,
        proxy_client: AsyncClient | None,
    ) -> str:
        """
        Авторизация в TMA Hamster Kombat через Telegram WebApp.

        :param raw_initdata: Сырые данные инициализации.
        :param user_agent: User-Agent.
        :param proxy_client: Клиент с Proxy сервером.
        :return: Токен авторизации.
        """
        cl = proxy_client or self._httpx_client
        res = await cl.post(
            f"{self._base_core}/auth/auth-by-telegram-webapp",
            headers=self.__get_headers(None, user_agent),
            json={"initDataRaw": raw_initdata},
        )
        if proxy_client is not None:
            await proxy_client.aclose()

        if res.status_code == 400:
            raise ApiError.bad_request(ErrorsPhrases.NON_PLAYABLE_INITDATA_CORRUPTED, res.content)

        if '"authToken":"' not in res.text:
            raise ApiError.failed_dependency(ErrorsPhrases.HAMSTER_UNEXPECTED_AUTH_REPONSE, res.content, True)

        return res.text.split('"authToken":"')[1].split('"')[0]

    async def sync(
        self,
        token: str,
        user_agent: str,
        proxy_client: AsyncClient | None,
    ) -> ClickerUserDict:
        """
        Получить данные пользователя.

        :param token: Токен авторизации.
        :param user_agent: User-Agent.
        :param proxy_client: Клиент с Proxy сервером.
        :return: Данные пользователя.
        """
        cl = proxy_client or self._httpx_client
        res = await cl.post(
            f"{self._base_url}/sync",
            headers=self.__get_headers(token, user_agent),
        )
        if proxy_client is not None:
            await proxy_client.aclose()

        res = res.raise_for_status()

        jres = {}
        fial_check = b'"clickerUser":{' not in res.content
        if not fial_check:
            jres = cast(dict[str, ClickerUserDict], await synct(orjson.loads)(res.content))
            fial_check = "clickerUser" not in jres

        if fial_check:
            raise ApiError.failed_dependency(
                ErrorsPhrases.HAMSTER_CLIENT_ERROR,
                (res.status_code, res.content),
            )

        return jres["clickerUser"]

    async def tap_hamster(
        self,
        token: str,
        user_agent: str,
        proxy_client: AsyncClient | None,
        count: int,
        available_taps: int,
    ) -> ClickerUserDict:
        """
        Тапнуть хомяка.

        :param token: Токен авторизации.
        :param user_agent: User-Agent.
        :param proxy_client: Клиент с Proxy сервером.
        :param count: Количество тапов.
        :param available_taps: Доступные тапы.
        :return: Данные пользователя.
        """
        cl = proxy_client or self._httpx_client
        res = await cl.post(
            f"{self._base_url}/tap",
            headers=self.__get_headers(token, user_agent),
            json={
                "count": count,
                "availableTaps": available_taps,
                "timestamp": int(time.time()),
            },
        )
        if proxy_client is not None:
            await proxy_client.aclose()

        res = res.raise_for_status()

        jres = {}
        fial_check = b'"clickerUser":{' not in res.content
        if not fial_check:
            jres = cast(dict[str, ClickerUserDict], await synct(orjson.loads)(res.content))
            fial_check = "clickerUser" not in jres

        if fial_check:
            raise ApiError.failed_dependency(
                ErrorsPhrases.HAMSTER_CLIENT_ERROR,
                (res.status_code, res.content),
            )

        return jres["clickerUser"]

    async def get_tasks(
        self,
        token: str,
        user_agent: str,
        proxy_client: AsyncClient | None,
    ) -> list[ClickerTaskDict]:
        """
        Получить список задач.

        :param token: Токен авторизации.
        :param user_agent: User-Agent.
        :param proxy_client: Клиент с Proxy сервером.
        :return: Список задач.
        """
        cl = proxy_client or self._httpx_client
        res = await cl.post(
            f"{self._base_url}/list-tasks",
            headers=self.__get_headers(token, user_agent),
        )
        if proxy_client is not None:
            await proxy_client.aclose()

        res = res.raise_for_status()

        jres = {}
        fial_check = b'"tasks":[' not in res.content
        if not fial_check:
            jres = cast(dict[str, list[ClickerTaskDict]], await synct(orjson.loads)(res.content))
            fial_check = "tasks" not in jres

        if fial_check:
            raise ApiError.failed_dependency(
                ErrorsPhrases.HAMSTER_CLIENT_ERROR,
                (res.status_code, res.content),
            )

        return jres["tasks"]

    async def complete_task(
        self,
        token: str,
        user_agent: str,
        proxy_client: AsyncClient | None,
        task_id: str,
    ) -> ClickerUserDict:
        """
        Завершить задачу.

        :param token: Токен авторизации.
        :param user_agent: User-Agent.
        :param proxy_client: Клиент с Proxy сервером.
        :param task_id: Идентификатор задачи.
        :return: True, если задачи есть, иначе False.
        """
        cl = proxy_client or self._httpx_client
        res = await cl.post(
            f"{self._base_url}/check-task",
            headers=self.__get_headers(token, user_agent),
            json={"taskId": task_id},
        )
        if proxy_client is not None:
            await proxy_client.aclose()

        res = res.raise_for_status()

        jres = {}
        fial_check = b'"clickerUser":{' not in res.content
        if not fial_check:
            jres = cast(dict[str, ClickerUserDict], await synct(orjson.loads)(res.content))
            fial_check = "clickerUser" not in jres

        if fial_check:
            raise ApiError.failed_dependency(
                ErrorsPhrases.HAMSTER_CLIENT_ERROR,
                (res.status_code, res.content),
            )

        return jres["clickerUser"]

    async def get_upgrades_list(
        self,
        token: str,
        user_agent: str,
        proxy_client: AsyncClient | None,
    ) -> tuple[list[ClickerUpgradeDict], ClickerDailyComboDict]:
        """
        Получить список апгрейдов.

        :param token: Токен авторизации.
        :param user_agent: User-Agent.
        :param proxy_client: Клиент с Proxy сервером.
        :return: Список апгрейдов.
        """
        cl = proxy_client or self._httpx_client
        res = await cl.post(
            f"{self._base_url}/upgrades-for-buy",
            headers=self.__get_headers(token, user_agent),
        )
        if proxy_client is not None:
            await proxy_client.aclose()

        res = res.raise_for_status()

        jres = {}
        fial_check = b'"upgradesForBuy":[' not in res.content
        if not fial_check:
            jres = cast(
                dict[str, list[ClickerUpgradeDict] | ClickerDailyComboDict],
                await synct(orjson.loads)(res.content),
            )
            fial_check = "upgradesForBuy" not in jres

        if fial_check:
            raise ApiError.failed_dependency(
                ErrorsPhrases.HAMSTER_CLIENT_ERROR,
                (res.status_code, res.content),
            )

        return (
            cast(list[ClickerUpgradeDict], jres["upgradesForBuy"]),
            cast(ClickerDailyComboDict, jres["dailyCombo"]),
        )

    async def buy_upgrade(
        self,
        token: str,
        user_agent: str,
        proxy_client: AsyncClient | None,
        upgrade_id: str,
    ) -> tuple[ClickerUserDict, list[ClickerUpgradeDict], ClickerDailyComboDict]:
        """
        Купить апгрейд.

        :param token: Токен авторизации.
        :param user_agent: User-Agent.
        :param proxy_client: Клиент с Proxy сервером.
        :param upgrade_id: Идентификатор апгрейда.
        :return: Данные пользователя.
        """
        cl = proxy_client or self._httpx_client
        res = await cl.post(
            f"{self._base_url}/buy-upgrade",
            headers=self.__get_headers(token, user_agent),
            json={
                "upgradeId": upgrade_id,
                "timestamp": int(time.time()),
            },
        )
        if proxy_client is not None:
            await proxy_client.aclose()

        res = res.raise_for_status()

        jres = {}
        fial_check = b'"clickerUser":{' not in res.content
        if not fial_check:
            jres = cast(
                dict[str, ClickerUserDict | list[ClickerUpgradeDict] | ClickerDailyComboDict],
                await synct(orjson.loads)(res.content),
            )
            fial_check = "clickerUser" not in jres

        if fial_check:
            raise ApiError.failed_dependency(
                ErrorsPhrases.HAMSTER_CLIENT_ERROR,
                (res.status_code, res.content),
            )

        return (
            cast(ClickerUserDict, jres["clickerUser"]),
            cast(list[ClickerUpgradeDict], jres["upgradesForBuy"]),
            cast(ClickerDailyComboDict, jres["dailyCombo"]),
        )
