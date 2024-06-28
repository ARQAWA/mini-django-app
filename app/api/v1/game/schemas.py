from ninja import Schema
from pydantic import Field


class SlotCreatePostBody(Schema):
    """Схема для создания слота игры."""

    payment_hash: str | None = Field(title="Хэш платежа")


class AccountLinkPutBody(Schema):
    """Схема для обновления слота игры."""

    tg_id: int = Field(title="Telegram ID")
    first_name: str = Field(title="Имя")
    last_name: str | None = Field(title="Фамилия")
    username: str | None = Field(title="Username")

    init_data: str = Field(title="Инициализационные данные")
    proxy: str | None = Field(title="Прокси")
