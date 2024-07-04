from app.core.common.singleton import SingletonMeta
from app.core.libs.httpx_ import httpx_client


class HamsterKombatClient(metaclass=SingletonMeta):
    """Клиент для игры в игру Hamster Kombat."""

    def __init__(self) -> None:
        self.__httpx = httpx_client

    async def sync(self) -> None:
        """Синхронизация аккаунта."""
