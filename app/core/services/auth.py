import asyncio

import orjson

from app.core.clients.redis_ import redis_client
from app.core.common.tg_auth import sync_create_auth_token, sync_get_user_obj
from app.core.envs import envs
from app.core.error import ApiError
from app.core.executors import XQTR_P, XQTR_T
from app.core.models.tg_user_data import PlayerData
from app.core.repositories.user import UserRepository
from app.core.singleton import SingletonMeta


class AuthService(metaclass=SingletonMeta):
    """Сервис авторизации."""

    def __init__(self) -> None:
        self._redis_client = redis_client
        self._user_repo = UserRepository()

    async def authorize(self, init_data: str, user_agent: str) -> str:
        """
        Получение данных пользователя.

        :param init_data: Данные инициализации
        :param user_agent: User-Agent
        :return: токен пользователя
        """
        ev_loop = asyncio.get_event_loop()

        try:
            user_obj = await ev_loop.run_in_executor(
                XQTR_P,
                sync_get_user_obj,
                init_data,
                envs.telegram_bot.token,
            )
        except Exception as err:
            if not isinstance(err, ApiError):
                raise ApiError.unauthorized(with_sentry=True) from err
            raise

        user_token = await ev_loop.run_in_executor(XQTR_P, sync_create_auth_token, user_obj["id"], user_agent)
        user_obj_string = await ev_loop.run_in_executor(XQTR_T, orjson.dumps, user_obj)
        await self._user_repo.set_user(user_token, user_obj_string)

        return user_token

    async def get_user_info(self, auth_token: str) -> PlayerData.Dict:
        """
        Получение данных пользователя.

        :param auth_token: токен пользователя
        :return: данные пользователя
        """
        user_dict = await self._user_repo.get_user(auth_token)
        if user_dict is None:
            raise ApiError.unauthorized()

        return user_dict
