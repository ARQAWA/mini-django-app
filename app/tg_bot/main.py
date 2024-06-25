import asyncio

import sentry_sdk
from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramNetworkError
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    Message,
)
from loguru import logger

from app.core.envs import envs
from app.core.services.tg_auth import TgAuthService


class MiniAppHolderBot:
    """Класс для работы с ботом-держателем мини-приложения."""

    def __init__(self) -> None:
        self._bot = Bot(envs.telegram_bot.token)
        self._dispatcher = Dispatcher()
        self._setup_handlers()
        self._tg_auth_svc = TgAuthService()

    async def bootstrap(self) -> None:
        """Запуск бота."""
        logger.debug("Запуск бота-держателя мини-приложения.")
        await self._dispatcher.start_polling(self._bot, polling_timeout=30)

    def _setup_handlers(self) -> None:
        """Настройка обработчиков."""

        @self._dispatcher.message(CommandStart())
        async def start(message: Message) -> None:
            """Обработчик команды /start."""
            if not message.from_user or message.from_user.is_bot:
                return

            while True:
                try:
                    await self._bot.send_message(
                        message.chat.id,
                        "WAZZUP! Send /auth_code to get the code.",
                        request_timeout=5,
                    )
                    break
                except TelegramNetworkError as err:
                    sentry_sdk.capture_exception(err)
                    logger.error(f"Ошибка при отправке сообщения: {err}")

        @self._dispatcher.message(Command("auth_code"))
        async def code(message: Message) -> None:
            """Обработчик команды /desktop_code."""
            if not message.from_user or message.from_user.is_bot:
                return

            answer = await self._tg_auth_svc.get_auth_hash(message.from_user)
            while True:
                try:
                    await self._bot.send_message(
                        message.chat.id,
                        f"The code is valid for 30 seconds:\n\n`{answer}`",
                        parse_mode="MarkdownV2",
                        request_timeout=5,
                    )
                    break
                except TelegramNetworkError as err:
                    sentry_sdk.capture_exception(err)
                    logger.error(f"Ошибка при отправке сообщения: {err}")


if __name__ == "__main__":
    from asyncio import CancelledError
    from contextlib import suppress

    import uvloop

    from app.core.common.sentry import sentry_init

    with suppress(KeyboardInterrupt, SystemExit, CancelledError):
        sentry_init()
        uvloop.install()
        asyncio.run(MiniAppHolderBot().bootstrap())
