from ninja import ModelSchema

from app.core.apps.users.models import Customer


class CustomerModelSchema(ModelSchema):
    """Схема модели покупателя."""

    class Meta:
        """Метаданные схемы."""

        model = Customer
        fields = ["id", "first_name", "last_name", "username"]
