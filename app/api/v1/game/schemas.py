from ninja import Schema
from pydantic import Field


class SlotCreatePostBody(Schema):
    """Схема для создания слота игры."""

    payment_hash: str | None = Field(title="Хэш платежа")


class AccountLinkPutBody(Schema):
    """Схема для обновления слота игры."""

    init_data: str = Field(title="Данные инициализации")
    proxy: str | None = Field(title="Прокси")
