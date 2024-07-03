from datetime import datetime

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

    proxy_url: str | None = Field(title="URL прокси")

    play_stats: PlayModelSchema = Field(alias="play", title="Статистика игры")
    network_stats: NetworkModelSchema = Field(alias="network", title="Статистика сети")

    is_playing: bool = Field(default=False, title="Играет ли аккаунт")

    class Meta:
        """Метаданные схемы."""

        model = Account
        exclude = ("id", "init_data", "auth_token", "user_agent", "game", "customer")


class SlotModelSchema(ModelSchema):
    """Схема модели слота."""

    id: int
    account: AccountModelSchema | None = None
    expired_at: datetime
    is_payed: bool = Field(default=False, alias="payment.is_payed", title="Оплачен ли слот")

    class Meta:
        """Метаданные схемы."""

        model = Slot
        fields = ("id", "account", "expired_at")
