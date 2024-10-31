from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.tg_bot.utils.cycler import send_loop


def msg_start(bot: Bot, dispatcher: Dispatcher) -> None:
    """Добавление обработчика команды /start."""

    @dispatcher.message(CommandStart())
    async def start(message: Message) -> None:
        """Обработчик команды /start."""
        if not message.from_user or message.from_user.is_bot:
            return

        with send_loop():
            await bot.send_message(message.chat.id, "WAZZUP! Send /auth_code to get the code.", request_timeout=5)
