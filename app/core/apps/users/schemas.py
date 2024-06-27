from ninja import ModelSchema

from app.core.apps.users.models import Customer
from app.core.common.ninjas_fix.renderers import Schema


class CustomerSchema(Schema):
    """Схема с данными покупателя."""

    id: int
    first_name: str
    last_name: str | None
    username: str | None
    has_trial: bool


class CustomerModelSchema(ModelSchema):
    """Схема модели покупателя."""

    class Meta:
        """Метаданные схемы."""

        model = Customer
        fields = ["id", "first_name", "last_name", "username", "has_trial"]
