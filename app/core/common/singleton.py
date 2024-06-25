from typing import Any


class SingletonMeta(type):
    """Singleton metaclass."""

    _instances: dict[type, type] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        """Create instance if not exists."""
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
