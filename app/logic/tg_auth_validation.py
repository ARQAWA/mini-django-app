import asyncio
import hashlib
import hmac
from typing import Optional, TypedDict, cast
from urllib.parse import unquote

import orjson
from ninja import Schema

from app.core.envs import envs
from app.core.executors import XQTR_P


class TgUser(TypedDict):
    """Схема словаря с данными пользователя."""

    id: int
    first_name: str
    added_to_attachment_menu: Optional[bool]
    allows_write_to_pm: Optional[bool]
    is_premium: Optional[bool]
    is_bot: Optional[bool]
    last_name: Optional[str]
    language_code: Optional[str]
    photo_url: Optional[str]
    username: Optional[str]


class TgUserSchema(Schema):
    """Схема с данными пользователя."""

    id: int
    first_name: str
    added_to_attachment_menu: Optional[bool] = None
    allows_write_to_pm: Optional[bool] = None
    is_premium: Optional[bool] = None
    is_bot: Optional[bool] = None
    last_name: Optional[str] = None
    language_code: Optional[str] = None
    photo_url: Optional[str] = None
    username: Optional[str] = None


async def get_user_object(init_data: str) -> TgUser:
    """
    Асинхронный метод для получения объекта пользователя.

    :param init_data: Данные инициализации
    :return: Словарь с данными пользователя.
    """
    return await asyncio.get_event_loop().run_in_executor(
        XQTR_P,
        __get_user_obj_with_validation,
        init_data,
        envs.telegram_bot.token,
    )


def __get_user_obj_with_validation(init_data: str, token: str) -> TgUser:
    """Валидация данных инициализации."""
    user_object = None

    hash_value = ""
    joined_pairs = b""

    for pair_line in sorted(init_data.split("&")):
        if pair_line.startswith("hash="):
            hash_value = pair_line[5:]
            continue

        key, value = unquote(pair_line).split("=", 1)
        joined_pairs += f"{key}={value}\n".encode()

        if key == "user" and not isinstance(user_object := orjson.loads(value), dict):
            raise TgAuthDataError("User object is not a dictionary.")

    if user_object is None:
        raise TgAuthDataError("User object not found.")

    bot_secret = hmac.new(
        b"WebAppData",
        token.encode(),
        hashlib.sha256,
    ).digest()

    calculated_hash = hmac.new(
        bot_secret,
        joined_pairs.strip(),
        hashlib.sha256,
    ).hexdigest()

    if hash_value != calculated_hash:
        raise TgAuthValidationError("Incorrect hash value.")

    return cast(TgUser, user_object)


class TgAuthError(Exception):
    """Базовый класс ошибки авторизации."""


class TgAuthValidationError(TgAuthError):
    """Ошибка валидации данных авторизации."""


class TgAuthDataError(TgAuthError):
    """Ошибка формата данных авторизации."""


__all__ = [
    "get_user_object",
    "TgUser",
    "TgUserSchema",
    "TgAuthError",
    "TgAuthValidationError",
    "TgAuthDataError",
]
