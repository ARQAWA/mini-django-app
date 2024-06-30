from app.core.common.enums import ErrorsPhrases
from app.core.common.error import ApiError
from app.core.common.singleton import SingletonMeta
from app.core.libs.httpx_ import httpx_client


class TMAHamsterKombat(metaclass=SingletonMeta):
    """Клиент для работы с TMA Hamster Kombat."""

    _base_core = "https://api.hamsterkombat.io"
    _base_url = f"{_base_core}/clicker"

    def __init__(self) -> None:
        self._httpx_client = httpx_client

    async def auth_tg_webapp(self, raw_initdata: str, user_agent: str) -> str:
        """
        Авторизация в TMA Hamster Kombat через Telegram WebApp.

        :param raw_initdata: Сырые данные инициализации.
        :param user_agent: User-Agent.
        :return: Токен авторизации.
        """
        res = await self._httpx_client.post(
            f"{self._base_core}/auth/auth-by-telegram-webapp",
            headers=self.__get_headers(None, user_agent),
            json={"initDataRaw": raw_initdata},
        )

        if res.status_code == 400:
            raise ApiError.bad_request(ErrorsPhrases.NON_PLAYABLE_INITDATA_CORRUPTED, res.content)

        if '"authToken":"' not in res.text:
            raise ApiError.failed_dependency(ErrorsPhrases.HAMSTER_UNEXPECTED_AUTH_REPONSE, res.content, True)

        return res.text.split('"authToken":"')[1].split('"')[0]

    @staticmethod
    def __get_headers(token: str | None, user_agent: str) -> dict[str, str]:
        """Получить заголовки для запроса к TMA Hamster Kombat."""
        return {
            "User-Agent": user_agent,
            "Authorization": ("Bearer " + token) if token is not None else "authToken is empty, store token null",
            "Origin": "https://hamsterkombat.io",
            "Referer": "https://hamsterkombat.io/",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
        }
