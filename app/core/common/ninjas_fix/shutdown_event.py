import asyncio
import signal
from asyncio import AbstractEventLoop

from app.core.envs import envs
from app.core.libs.shutdown_container import shutdown_container

SHUTDOWN_LOCK = asyncio.Lock()
CALLED = False


def setup_shutdown_event() -> None:
    """Установка обработчиков сигналов завершения."""
    if envs.is_local:
        return

    ev_loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGQUIT, signal.SIGHUP, signal.SIGABRT):
        ev_loop.add_signal_handler(sig, lambda: ev_loop.create_task(shutdown(sig, ev_loop)))


async def shutdown(sig: signal.Signals, event_loop: AbstractEventLoop) -> None:
    """Завершение работы приложения."""
    global CALLED

    async with SHUTDOWN_LOCK:
        if CALLED:
            return

        CALLED = True
        await shutdown_container.shutdown()

        # Отмена всех задач и остановка цикла событий
        for task in asyncio.all_tasks(event_loop):
            task.cancel("Shutdown application")
