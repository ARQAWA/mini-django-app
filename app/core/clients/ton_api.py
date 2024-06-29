import time
from typing import TYPE_CHECKING

import loguru
import orjson

from app.core.common.error import ApiError
from app.core.common.executors import syncp
from app.core.common.singleton import SingletonMeta
from app.core.envs import envs
from app.core.libs.httpx_ import httpx_client

if TYPE_CHECKING:
    from ninja.types import DictStrAny


class TonApiClient(metaclass=SingletonMeta):
    """Клиент для работы с TON Blockchain API."""

    _base_url = envs.ton_client.base_url
    _payment_address = envs.ton_client.payment_address

    _urls = {
        "get_transactions": "/v2/blockchain/accounts/{address}/transactions?limit=100&sort_order=desc",
    }

    _headers = {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
    }

    def __init__(self) -> None:
        self._httpx_client = httpx_client

    async def get_payed_list(self) -> list[str]:
        """Получение списка проведенных платежей."""
        url = f"{self._base_url}{self._urls["get_transactions"].format(address=self._payment_address)}"

        try:
            last = time.time()
            response = await self._httpx_client.get(url, headers=self._headers)
            last = time.time() - last
            loguru.logger.debug(f"GET {url} / {last:.3f}s. / - {response.status_code} - {response.text[:32]}")
            response.raise_for_status()
            jres: list[str] = await syncp(process_transactions_reponse)(response.content)
            return jres
        except Exception as err:
            raise ApiError.failed_dependency(f"Failed to get payed list: {err}") from err


def process_transactions_reponse(response: bytes) -> list[str]:
    """Обработка ответа с данными о транзакциях."""
    data: DictStrAny = orjson.loads(response)

    if not isinstance(data, dict):
        raise ValueError("Invalid response data")

    processed_data = [
        item.get("in_msg", {}).get("decoded_body", {}).get("text", None)
        for item in data.get("transactions", [])
        if item.get("success", False)
    ]

    return processed_data
