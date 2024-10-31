import asyncio
from asyncio import AbstractEventLoop
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from typing import Any, Callable, Coroutine, TypeVar

__XQTR_T: ThreadPoolExecutor | None = None
__XQTR_P: ProcessPoolExecutor | None = None

TCallable = TypeVar("TCallable", bound=Callable[..., Any])


def get_thread_pool() -> ThreadPoolExecutor:
    """Get thread pool executor."""
    global __XQTR_T
    if not __XQTR_T:
        __XQTR_T = ThreadPoolExecutor()
    return __XQTR_T


def get_process_pool() -> ProcessPoolExecutor:
    """Get process pool executor."""
    global __XQTR_P
    if not __XQTR_P:
        __XQTR_P = ProcessPoolExecutor()
    return __XQTR_P


def synct(func: TCallable, event_loop: AbstractEventLoop | None = None) -> Callable[..., Coroutine[Any, Any, Any]]:
    """Run function in thread pool executor."""

    async def wrapper(*args: Any) -> Any:
        if event_loop:
            return await event_loop.run_in_executor(get_thread_pool(), func, *args)
        return await asyncio.get_running_loop().run_in_executor(get_thread_pool(), func, *args)

    return wrapper


def syncp(func: TCallable, event_loop: AbstractEventLoop | None = None) -> Callable[..., Coroutine[Any, Any, Any]]:
    """Run function in process pool executor."""

    async def wrapper(*args: Any) -> Any:
        if event_loop:
            return await event_loop.run_in_executor(get_process_pool(), func, *args)
        return await asyncio.get_running_loop().run_in_executor(get_process_pool(), func, *args)

    return wrapper


__all__ = ["synct", "syncp", "get_thread_pool", "get_process_pool"]
