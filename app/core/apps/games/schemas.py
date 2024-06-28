from datetime import UTC, datetime

from ninja import ModelSchema
from pydantic import Field

from app.core.apps.games.models import Account, Slot
from app.core.apps.stats.schemas import NetworkModelSchema, PlayModelSchema


class AccountModelSchema(ModelSchema):
    """Схема модели аккаунта."""

    tg_id: int = Field(title="Telegram ID")
    first_name: str = Field(title="Имя")
    last_name: str | None = Field(title="Фамилия")
    username: str | None = Field(title="Username")

    init_data: str = Field(title="Данные инициализации")
    proxy_url: str | None = Field(title="URL прокси")

    play_stats: PlayModelSchema = Field(alias="play", title="Статистика игры")
    network_stats: NetworkModelSchema = Field(alias="network", title="Статистика сети")

    is_playing: bool = Field(title="Играет ли аккаунт")

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
