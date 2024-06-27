from typing import TypedDict

from ninja.types import DictStrAny

from app.core.common.ninjas_fix.renderers import Schema


class UserData(Schema):
    """Схема с данными пользователя."""

    id: int
    first_name: str
    last_name: str | None = None
    username: str | None = None
    has_trial: bool

    class Dict(TypedDict):
        """Схема словаря с данными пользователя."""

        id: int
        first_name: str
        last_name: str | None
        username: str | None
        has_trial: bool

    @staticmethod
    def ninja_result(obj: Dict) -> DictStrAny:
        """Возвращает результат."""
        return Schema.ninja_result(obj)
