import asyncio
from typing import Callable

from aiogram import Bot, Dispatcher
from loguru import logger

from app.core.envs import envs
from app.tg_bot.handlers.auth_code import msg_auth_code
from app.tg_bot.handlers.start import msg_start


class MiniAppHolderBot:
    """Класс для работы с ботом-держателем мини-приложения."""

    def __init__(self) -> None:
        self._bot = Bot(envs.telegram_bot.token)
        self._dispatcher = Dispatcher()

        self.__register_handler(msg_start)
        self.__register_handler(msg_auth_code)

    async def bootstrap(self) -> None:
        """Запуск бота."""
        logger.debug("Запуск бота-держателя мини-приложения.")
        await self._dispatcher.start_polling(self._bot, polling_timeout=30)

    def __register_handler(self, func: Callable[[Bot, Dispatcher], None]) -> None:
        """Регистрация обработчика."""
        func(self._bot, self._dispatcher)


if __name__ == "__main__":
    from asyncio import CancelledError
    from contextlib import suppress

    import uvloop

    from app.core.common.sentry import sentry_init

    with suppress(KeyboardInterrupt, SystemExit, CancelledError):
        sentry_init()
        uvloop.install()
        asyncio.run(MiniAppHolderBot().bootstrap())
