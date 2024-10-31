from typing import cast

from app.core.common.singleton import SingletonMeta
from app.core.envs import envs
from app.core.libs.redis_ import redis_client


class TgAuthRepo(metaclass=SingletonMeta):
    """Репозиторий авторизации Telegram."""

    _hash_key = "auth:tg:user_hash:"
    _user_key = "auth:tg:hash_user:"

    def __init__(self) -> None:
        self._redis_client = redis_client

    async def set_auth_hash(self, user_id: int, auth_hash: bytes) -> None:
        """
        Установка хэша авторизации пользователя.

        :param user_id: id пользователя
        :param auth_hash: хэш авторизации
        """
        await self._redis_client.set(self._hash_key + str(user_id), auth_hash, ex=envs.auth.auth_token_ttl)

    async def get_auth_hash(self, user_id: int) -> bytes | None:
        """
        Получение хэша авторизации пользователя.

        :param user_id: id пользователя
        :return: хэш авторизации
        """
        return cast(bytes | None, await self._redis_client.get(self._hash_key + str(user_id)))

    async def delete_auth_data(self, user_id: int, auth_hash: bytes) -> None:
        """
        Удаление хэша авторизации пользователя.

        :param user_id: id пользователя
        :param auth_hash: хэш авторизации
        """
        await self._redis_client.delete(self._hash_key + str(user_id))
        await self._redis_client.delete(self._user_key + str(auth_hash))

    async def set_user_string_by_hash(self, auth_hash: bytes, user_json: bytes) -> None:
        """
        Установка данных пользователя по хешу авторизации.

        :param auth_hash: хеш авторизации
        :param user_json: данные пользователя
        """
        await self._redis_client.set(self._user_key + str(auth_hash), user_json, ex=envs.auth.auth_token_ttl)

    async def get_user_string_by_hash(self, auth_hash: bytes) -> bytes | None:
        """
        Получение данных пользователя по хэшу авторизации.

        :param auth_hash: хеш авторизации
        :return: данные пользователя
        """
        return cast(bytes | None, await self._redis_client.get(self._user_key + str(auth_hash)))
