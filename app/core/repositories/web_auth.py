from typing import cast

from app.core.clients.redis_ import redis_client
from app.core.common.singleton import SingletonMeta
from app.core.envs import envs


class WebAuthRepo(metaclass=SingletonMeta):
    """Репозиторий авторизации веб-пользователей."""

    _access_key = "auth:web:access:"
    _refresh_blocked_key = "auth:web:refreshb:"

    def __init__(self) -> None:
        self._redis_client = redis_client

    async def set_access_token(self, access_token: bytes, user_id: int) -> None:
        """
        Запись access токена в Redis.

        :param access_token: access токен
        :param user_id: идентификатор пользователя
        """
        await self._redis_client.set(self._access_key + access_token.decode(), user_id, ex=envs.auth.access_token_ttl)

    async def get_user_by_access_token(self, access_token: bytes) -> bytes | None:
        """
        Получение данных пользователя по access токену.

        :param access_token: access токен
        :return: данные пользователя
        """
        return cast(bytes | None, await self._redis_client.get(self._access_key + access_token.decode()))

    async def block_refresh_token(self, refresh_token: bytes) -> None:
        """
        Блокировка refresh токена.

        :param refresh_token: refresh токен
        """
        await self._redis_client.set(
            self._refresh_blocked_key + refresh_token.decode(),
            b"blocked",
            ex=envs.auth.refresh_token_ttl,
        )

    async def is_blocked(self, refresh_token: bytes) -> int:
        """
        Проверка на блокировку refresh токена.

        :param refresh_token: refresh токен
        :return: True, если токен заблокирован, иначе False
        """
        return cast(int, await self._redis_client.exists(self._refresh_blocked_key + refresh_token.decode()))
