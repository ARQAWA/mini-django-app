from ninja import ModelSchema

from app.core.apps.stats.models import Network, Play


class PlayModelSchema(ModelSchema):
    """Схема статистики игры."""

    class Meta:
        """Метаданные схемы."""

        model = Play
        fields = "__all__"


class NetworkModelSchema(ModelSchema):
    """Схема статистики сети."""

    class Meta:
        """Метаданные схемы."""

        model = Network
        fields = "__all__"
