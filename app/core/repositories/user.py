import asyncio

import orjson
import sentry_sdk
from redis import ConnectionError, RedisError, TimeoutError

from app.core.clients.redis_ import redis_client
from app.core.envs import envs
from app.core.executors import XQTR_T
from app.core.models.tg_user_data import PlayerData
from app.core.singleton import SingletonMeta


class UserRepository(metaclass=SingletonMeta):
    """Репозиторий пользователей."""

    def __init__(self) -> None:
        self._redis_client = redis_client

    async def set_user(self, user_token: str, user_obj_string: bytes) -> None:
        """
        Запись данных пользователя в Redis.

        :param user_token: токен пользователя
        :param user_obj_string: строка с данными пользователя
        """
        try:
            for _ in range(3):
                await self._redis_client.set(
                    user_token,
                    user_obj_string,
                    ex=envs.auth.token_ttl,
                )
                break
        except (ConnectionError, TimeoutError):
            pass
        except RedisError as err:
            sentry_sdk.capture_exception(err)
            return

    async def get_user(self, auth_token: str) -> PlayerData.Dict | None:
        """
        Получение данных пользователя из Redis.

        :param auth_token: токен пользователя
        :return: данные пользователя
        """
        try:
            for _ in range(3):
                user_obj_string = await self._redis_client.get(auth_token)
                if user_obj_string is None:
                    return None
                return await asyncio.get_event_loop().run_in_executor(XQTR_T, orjson.loads, user_obj_string)
            return None
        except (ConnectionError, TimeoutError):
            return None
        except RedisError as err:
            sentry_sdk.capture_exception(err)
            return None
