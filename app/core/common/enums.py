from enum import Enum, StrEnum


class ModelEnum(Enum):
    """Базовый класс для перечислений моделей."""

    @classmethod
    def choices(cls) -> list[tuple[str, str]]:
        """Получение имени модели."""
        return [(type_.name, type_.value) for type_ in cls]


class ErrorsPhrases(StrEnum):
    """Строки ошибок."""

    SLOT_NOT_FOUND = "SLOT_NOT_FOUND"  # слот не найден
    ACCOUNT_NOT_FOUND = "ACCOUNT_NOT_FOUND"  # аккаунт не найден
    ANOTHER_USER_LINKED = "ANOTHER_USER_LINKED"  # аккаунт уже привязан к другому пользователю
    ANOTHER_SLOT_LINKED = "ANOTHER_SLOT_LINKED"  # аккаунт уже привязан к другому слоту
    DEMO_SLOT_NOT_AVAILABLE = "DEMO_SLOT_NOT_AVAILABLE"  # демо слот недоступен
    PAYMENT_EXTENSION_NOT_ALLOWED = "PAYMENT_EXTENSION_NOT_ALLOWED"  # продление платежа недоступно
