import contextlib
from asyncio import CancelledError
from typing import Generator

import sentry_sdk
from aiogram.exceptions import TelegramNetworkError
from loguru import logger


@contextlib.contextmanager
def send_loop() -> Generator[None, None, None]:
    """Контекстный менеджер для повторной отправки сообщения при ошибке."""
    try:
        while True:
            try:
                yield
                return
            except TelegramNetworkError as err:
                sentry_sdk.capture_exception(err)
                logger.error(f"Ошибка при отправке сообщения: {err}")
                return
            except (KeyboardInterrupt, SystemExit, CancelledError):
                return
            except Exception as err:
                sentry_sdk.capture_exception(err)
                logger.exception(f"Неизвестная ошибка при отправке сообщения: {err}")
                return
    finally:
        ...
