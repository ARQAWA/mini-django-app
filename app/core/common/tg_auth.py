import hashlib
import hmac
import time
from urllib.parse import unquote

import orjson

from app.core.error import ApiError
from app.core.models.tg_user_data import PlayerData


def sync_get_user_obj(init_data: str, token: str) -> PlayerData.Dict:
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
            raise ApiError.unauthorized(details="User object is not a dictionary.")

    if user_object is None:
        raise ApiError.unauthorized(details="User object not found.")

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
        raise ApiError.unauthorized(details="Incorrect hash value.")

    return {
        "id": user_object["id"],
        "first_name": user_object["first_name"],
        "last_name": user_object.get("last_name"),
        "username": user_object.get("username"),
        "photo_url": user_object.get("photo_url"),
        "is_bot": user_object.get("is_bot", False),
        "is_premium": user_object.get("is_premium", False),
        "language_code": user_object.get("language_code", "en"),
    }


def sync_create_auth_token(user_id: int, user_agent: str) -> str:
    """Создание токена авторизации."""
    stamp = int(time.time())
    finger_print = hashlib.md5(f"{user_id}{user_agent}{stamp}".encode()).hexdigest()
    return f"{stamp}{finger_print}{user_id}"
