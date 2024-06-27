from ninja import ModelSchema

from app.core.apps.games.models import Account, Info, Slot


class InfoModelSchema(ModelSchema):
    """Схема модели информации."""

    class Meta:
        """Метаданные схемы."""

        model = Info
        fields = "__all__"
        exclude = ("id",)


class AccountModelSchema(ModelSchema):
    """Схема модели аккаунта."""

    info: InfoModelSchema

    class Meta:
        """Метаданные схемы."""

        model = Account
        exclude = ("id",)


class SlotModelSchema(ModelSchema):
    """Схема модели слота."""

    account: AccountModelSchema | None = None

    class Meta:
        """Метаданные схемы."""

        model = Slot
        fields = ("id", "account", "expired_at")
