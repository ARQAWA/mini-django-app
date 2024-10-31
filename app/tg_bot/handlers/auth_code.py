from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from app.core.envs import envs
from app.core.services.tg_auth import TgAuthService
from app.tg_bot.utils.cycler import send_loop


def msg_auth_code(bot: Bot, dispatcher: Dispatcher) -> None:
    """Добавление обработчика команды /auth_code."""
    mins = envs.auth.auth_token_ttl // 60
    secs = envs.auth.auth_token_ttl % 60
    expires = " ".join((f"{mins} min" if mins else "", f"{secs} sec" if secs else "")).strip()
    template = f"The code is valid for {expires}:\n\n`{{}}`"

    @dispatcher.message(Command("auth_code"))
    async def code(message: Message) -> None:
        """Обработчик команды /desktop_code."""
        if not message.from_user or message.from_user.is_bot:
            return

        auth_token = await TgAuthService().get_auth_hash(message.from_user)
        response = template.format(auth_token)
        with send_loop():
            await bot.send_message(message.chat.id, response, parse_mode="MarkdownV2", request_timeout=5)
