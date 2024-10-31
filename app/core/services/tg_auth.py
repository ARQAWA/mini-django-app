import string

import orjson
from aiogram.types import User

from app.core.common.executors import syncp, synct
from app.core.common.gen_random_string import sync_get_rand_string
from app.core.common.singleton import SingletonMeta
from app.core.repositories.tg_auth import TgAuthRepo


class TgAuthService(metaclass=SingletonMeta):
    """Сервис авторизации в телеграме."""

    def __init__(self) -> None:
        self._tg_auth_repo = TgAuthRepo()
        self._symbols = string.ascii_letters + string.digits + "#+-.:@_|"

    async def get_auth_hash(self, user: User) -> str:
        """
        Получение хэша авторизации пользователя.

        Если хэш уже существует, то возвращается он.
        Иначе, создается новый хэш, сохраняется в базе данных и возвращается.

        :param user: Пользователь.
        :return: Хэш авторизации.
        """
        auth_hash_: bytes | None = await self._tg_auth_repo.get_auth_hash(user.id)
        if auth_hash_ is not None:
            return auth_hash_.decode()

        user_dict = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
        }

        auth_hash: bytes = await syncp(sync_get_rand_string)()
        user_json: bytes = await synct(orjson.dumps)(user_dict)

        await self._tg_auth_repo.set_auth_hash(user.id, auth_hash)
        await self._tg_auth_repo.set_user_string_by_hash(auth_hash, user_json)

        return auth_hash.decode()
