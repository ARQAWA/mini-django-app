from typing import Any, Callable, Coroutine, TypeVar

from httpx import HTTPStatusError
from loguru import logger

from app.core.common.executors import synct
from app.core.services.network_stats import write_network_stats
from app.tap_robotics.hamster_kombat.checkout_session import write_checkpoint

TCallable = TypeVar("TCallable", bound=Callable[..., Any])


class FailResult:
    """Ошибочный результат выполнения функции."""


async def wrap_http_request(
    coro: Coroutine[Any, Any, Any],
    account_id: int,
    err_message: str,
    write_erros: bool = True,
) -> Any:
    """Обертка для выполнения HTTP запросов."""
    try:
        return await coro
    except HTTPStatusError as err:
        logger.error(f"{err_message}: {err}")
        if write_erros:
            await synct(write_network_stats)(account_id, 0, {str(err.response.status_code): 1})
            await synct(write_checkpoint)(account_id, True)
        return err
    except Exception as err:
        logger.error(f"{err_message}: {err}")
        return FailResult()
