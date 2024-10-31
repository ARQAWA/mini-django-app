from typing import Self

from ninja import Schema
from pydantic import Field, model_validator


class SlotCreatePostBody(Schema):
    """Схема для создания слота игры."""

    slot_id: int | None = Field(title="ID слота")
    payment_hash: str | None = Field(title="Хэш платежа")

    @model_validator(mode="after")
    def root_validator(self) -> Self:
        """Валидация данных."""
        if self.slot_id is not None and self.payment_hash is None:
            raise ValueError("`payment_hash` is required if `slot_id` is provided")
        return self

    @property
    def is_demo(self) -> bool:
        """Запрос на демо-режим."""
        return self.slot_id is None and self.payment_hash is None


class AccountLinkPutBody(Schema):
    """Схема для обновления слота игры."""

    tg_id: int = Field(title="Telegram ID")
    first_name: str = Field(title="Имя")
    last_name: str | None = Field(title="Фамилия")
    username: str | None = Field(title="Username")

    init_data: str = Field(title="Инициализационные данные")
    proxy: str | None = Field(title="Прокси")


class AccountSwitchPlayPostBody(Schema):
    """Схема для запуска/остановки аккаунта в слоте игры."""

    play: bool = Field(title="Запустить/остановить аккаунт")
