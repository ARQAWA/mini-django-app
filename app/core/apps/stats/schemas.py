from ninja import ModelSchema

from app.core.apps.stats.models import Network, Play


class PlayModelSchema(ModelSchema):
    """Схема статистики игры."""

    class Meta:
        """Метаданные схемы."""

        model = Play
        exclude = ("id", "account")


class NetworkModelSchema(ModelSchema):
    """Схема статистики сети."""

    class Meta:
        """Метаданные схемы."""

        model = Network
        exclude = ("id", "account")
