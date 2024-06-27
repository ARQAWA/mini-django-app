import asyncio
from typing import cast

import orjson
from ninja.types import DictStrAny

from app.core.apps.users.models import Customer
from app.core.common.executors import syncp, synct
from app.core.common.gen_random_string import sync_get_rand_string
from app.core.common.ninjas_fix.auth_dep import UNATHORIZED_ERROR
from app.core.common.singleton import SingletonMeta
from app.core.common.threaded_transaction import by_transaction
from app.core.repositories.tg_auth import TgAuthRepo
from app.core.repositories.web_auth import WebAuthRepo


class WebAuthService(metaclass=SingletonMeta):
    """Сервис авторизации."""

    def __init__(self) -> None:
        self._tg_auth_repo = TgAuthRepo()
        self._web_auth_repo = WebAuthRepo()

    async def get_user_by_access(self, access_token: str) -> DictStrAny:
        """
        Получение пользователя по токену.

        :param access_token: access токен
        :return: данные пользователя
        """
        user_str = await self._web_auth_repo.get_user_by_access_token(access_token.encode())
        if user_str is None:
            raise UNATHORIZED_ERROR

        return cast(DictStrAny, await synct(orjson.loads)(user_str))

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
        user_str = cast(bytes, await synct(orjson.dumps)(user.user_obj))
        await self._web_auth_repo.set_access_token(access, user_str)

        await self._tg_auth_repo.delete_auth_data(user.id, auth_hash.encode())

        return access.decode(), refresh.decode()

    async def refresh(self, refresh_token: str) -> tuple[str, str]:
        """
        Обновление токена.

        :param refresh_token: refresh токен
        :return: access, refresh токены
        """
        refresh_str = refresh_token.encode()

        is_blocked = await self._web_auth_repo.is_blocked(refresh_str)
        if is_blocked:
            raise UNATHORIZED_ERROR

        access, refresh = await self.__gen_tokens()
        user = await synct(self.__update_refresh_token)(refresh_str, refresh)
        if user is None:
            raise UNATHORIZED_ERROR

        user_str = await synct(orjson.dumps)(user.user_obj)
        await self._web_auth_repo.set_access_token(access, user_str)
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
        user: Customer
        user, _ = Customer.objects.get_or_create(  # noqa: F841
            id=user_obj["id"],
            defaults=dict(
                first_name=user_obj["first_name"],
                last_name=user_obj["last_name"],
                username=user_obj["username"],
                refresh_token="__temp__",
            ),
        )
        user.refresh_token = refresh.decode()
        user.save()
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
        user: Customer
        try:
            user = Customer.objects.get(refresh_token=refresh_old.decode())
            user.refresh_token = refresh_new.decode()
            user.save()
            return user
        except Customer.DoesNotExist:
            return None
