import asyncio
from typing import TYPE_CHECKING, cast

import orjson

from app.core.apps.core.models import Customer
from app.core.common.executors import syncp, synct
from app.core.common.gen_random_string import sync_get_rand_string
from app.core.common.ninjas_fix.auth_dep import UNATHORIZED_ERROR
from app.core.common.singleton import SingletonMeta
from app.core.common.threaded_transaction import by_transaction
from app.core.repositories.tg_auth import TgAuthRepo
from app.core.repositories.web_auth import WebAuthRepo

if TYPE_CHECKING:
    from ninja.types import DictStrAny


class WebAuthService(metaclass=SingletonMeta):
    """Сервис авторизации."""

    def __init__(self) -> None:
        self._tg_auth_repo = TgAuthRepo()
        self._web_auth_repo = WebAuthRepo()

    async def get_user_id_by_access(self, access_token: str) -> int | None:
        """
        Получение пользователя по токену.

        :param access_token: access токен
        :return: данные пользователя
        """
        res = await self._web_auth_repo.get_user_by_access_token(access_token.encode())

        if res is None or not res.isdigit():
            return None

        return int(res)

    @staticmethod
    async def get_user_by_id(user_id: int) -> Customer | None:
        """
        Получение пользователя по идентификатору.

        :param user_id: идентификатор пользователя
        :return: пользователь
        """
        try:
            return await Customer.objects.aget(id=user_id)
        except Customer.DoesNotExist:
            raise UNATHORIZED_ERROR

    async def authorize(self, auth_hash: str) -> tuple[str, str]:
        """
        Авторизация пользователя.

        :param auth_hash: hash авторизации
        :return: access, refresh токены
        """
        user_str = await self._tg_auth_repo.get_user_string_by_hash(auth_hash.encode())
        if user_str is None:
            raise UNATHORIZED_ERROR

        access, refresh = await self.__gen_tokens()
        user: Customer = await synct(self.__auth_user)(user_str, refresh)
        await self._web_auth_repo.set_access_token(access, user.id)
        await self._tg_auth_repo.delete_auth_data(user.id, auth_hash.encode())

        return access.decode(), refresh.decode()

    async def refresh(self, refresh_token: str) -> tuple[str, str]:
        """
        Обновление токена.

        :param refresh_token: refresh токен
        :return: access, refresh токены
        """
        is_blocked = await self._web_auth_repo.is_blocked(refresh_str := refresh_token.encode())
        if is_blocked:
            raise UNATHORIZED_ERROR

        access, refresh = await self.__gen_tokens()
        user: Customer = await synct(self.__update_refresh_token)(refresh_str, refresh)
        if user is None:
            raise UNATHORIZED_ERROR

        await self._web_auth_repo.set_access_token(access, user.id)
        await self._web_auth_repo.block_refresh_token(refresh_str)

        return access.decode(), refresh.decode()

    @staticmethod
    async def __gen_tokens() -> tuple[bytes, bytes]:
        """Генерация токенов."""
        return cast(
            tuple[bytes, bytes],
            await asyncio.gather(
                syncp(sync_get_rand_string)(64),
                syncp(sync_get_rand_string)(256),
            ),
        )

    @staticmethod
    @by_transaction
    def __auth_user(user_str: bytes, refresh: bytes) -> Customer:
        """
        Обновление пользователя.

        :param user_str: данные пользователя
        :param refresh: refresh токен
        :return: пользователь
        """
        user_obj: DictStrAny = orjson.loads(user_str)
        user, _ = Customer.objects.update_or_create(  # noqa: F841
            id=user_obj["id"],
            defaults=dict(
                first_name=user_obj["first_name"],
                last_name=user_obj["last_name"],
                username=user_obj["username"],
                refresh_token=refresh.decode(),
            ),
        )
        return user

    @staticmethod
    @by_transaction
    def __update_refresh_token(refresh_old: bytes, refresh_new: bytes) -> Customer | None:
        """
        Обновление пользователя.

        :param refresh_old: старый refresh токен
        :param refresh_new: новый refresh токен
        :return: пользователь
        """
        user: Customer | None = Customer.objects.filter(refresh_token=refresh_old.decode()).first()
        if user is None:
            return None

        user.refresh_token = refresh_new.decode()
        user.save()
        return user
