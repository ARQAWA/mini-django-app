from enum import Enum


class ModelEnum(Enum):
    """Базовый класс для перечислений моделей."""

    @classmethod
    def choices(cls) -> list[tuple[str, str]]:
        """Получение имени модели."""
        return [(type_.name, type_.value) for type_ in cls]
