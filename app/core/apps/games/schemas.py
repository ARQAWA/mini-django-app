from datetime import UTC, datetime

from ninja import ModelSchema
from pydantic import Field

from app.core.apps.games.models import Account, Info, Slot


class InfoModelSchema(ModelSchema):
    """Схема модели информации."""

    class Meta:
        """Метаданные схемы."""

        model = Info
        fields = "__all__"


class AccountModelSchema(ModelSchema):
    """Схема модели аккаунта."""

    init_data: str
    proxy_url: str
    telegram: InfoModelSchema = Field(alias="info")
    is_playing: bool = False

    class Meta:
        """Метаданные схемы."""

        model = Account
        exclude = ("id", "info", "auth_token")


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
