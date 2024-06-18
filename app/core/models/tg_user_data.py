from typing import Optional, TypedDict

from ninja import Schema


class PlayerData(Schema):
    """Схема с данными пользователя."""

    id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    photo_url: Optional[str] = None
    is_bot: bool
    is_premium: bool
    language_code: str

    class Dict(TypedDict):
        """Схема словаря с данными пользователя."""

        id: int
        first_name: str
        last_name: str
        username: str
        photo_url: str
        is_bot: bool
        is_premium: bool
        language_code: str
