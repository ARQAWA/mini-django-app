import asyncio
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from typing import Any, Callable, Coroutine, TypeVar

__XQTR_T = ThreadPoolExecutor()
__XQTR_P = ProcessPoolExecutor()

TCallable = TypeVar("TCallable", bound=Callable[..., Any])


def synct(func: TCallable) -> Callable[..., Coroutine[Any, Any, Any]]:
    """Run function in thread pool executor."""

    async def wrapper(*args: Any) -> Any:
        return await asyncio.get_running_loop().run_in_executor(__XQTR_T, func, *args)

    return wrapper


def syncp(func: TCallable) -> Callable[..., Coroutine[Any, Any, Any]]:
    """Run function in process pool executor."""

    async def wrapper(*args: Any) -> Any:
        return await asyncio.get_running_loop().run_in_executor(__XQTR_P, func, *args)

    return wrapper


__all__ = ["synct", "syncp"]
