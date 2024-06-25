from functools import wraps
from typing import Any, Callable, TypeVar

from django.db import connections, transaction

T = TypeVar("T", bound=Callable[..., Any])


# декоратор для транзакций
def by_transaction(func: T) -> T:
    """Декоратор для транзакций."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        with connections["default"].cursor(), transaction.atomic():
            return func(*args, **kwargs)

    return wrapper  # type: ignore
