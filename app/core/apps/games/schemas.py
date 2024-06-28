from datetime import UTC, datetime

from ninja import ModelSchema
from pydantic import Field

from app.core.apps.games.models import Account, Slot


class AccountModelSchema(ModelSchema):
    """Схема модели аккаунта."""

    tg_id: int = Field(description="Идентификатор аккаунта")
    first_name: str = Field(description="Имя")
    last_name: str | None = Field(description="Фамилия")
    username: str | None = Field(description="Логин")

    init_data: str = Field(description="Данные инициализации")
    proxy_url: str | None = Field(description="URL прокси")

    is_playing: bool = Field(description="Играет ли аккаунт")

    class Meta:
        """Метаданные схемы."""

        model = Account
        exclude = ("id", "auth_token", "game", "customer")


class SlotModelSchema(ModelSchema):
    """Схема модели слота."""

    id: int
    account: AccountModelSchema | None = None
    is_expired: bool

    @staticmethod
    def resolve_is_expired(obj: Slot) -> bool:
        """Получение информации о просроченности слота."""
        return obj.expired_at <= datetime.now(UTC)

    class Meta:
        """Метаданные схемы."""

        model = Slot
        fields = ("id", "account")
