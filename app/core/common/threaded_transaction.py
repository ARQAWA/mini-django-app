from functools import wraps
from typing import Any, Callable, TypeVar

import loguru
from django.db import connections, transaction

T = TypeVar("T", bound=Callable[..., Any])


# декоратор для транзакций
def by_transaction(func: T) -> T:
    """Декоратор для транзакций."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        with connections["default"].cursor() as cur, transaction.atomic():
            loguru.logger.debug(f"Transaction started (id: {id(cur)})")
            return func(*args, **kwargs)

    return wrapper  # type: ignore
