from typing import Any, Callable

from ninja import Router as NinjaRouter
from ninja.types import TCallable

from app.core.common.ninjas_fix.renderers import ErrorResponse

ERRORS_PACK = {num: ErrorResponse for num in (401, 403, 422, 500)}


class Router(NinjaRouter):
    """Класс роутера."""

    def api_operation(self, *args: Any, **kwargs: Any) -> Callable[[TCallable], TCallable]:
        """Декоратор операции API."""
        response = kwargs.get("response", {})
        response.update(ERRORS_PACK)
        kwargs["response"] = response

        return super().api_operation(*args, **kwargs)
