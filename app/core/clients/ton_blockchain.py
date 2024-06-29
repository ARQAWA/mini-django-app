# from app.core.common.singleton import SingletonMeta
# from app.core.libs.httpx_ import httpx_client
#
#
# class TonApiClient(metaclass=SingletonMeta):
#     """Клиент для работы с TON Blockchain API."""
#
#     _base_url = "https://tonapi.io"
#
#     def __init__(self) -> None:
#         self._httpx_client = httpx_client
#
#     async def get_payed_list(self, address: str) -> dict:
#         """Получение списка проведенных платежей."""
#         response = self._httpx_client.get(
#             f"{self._base_url}/v2/payments/{address}",
#         )
#         response.raise_for_status()
#         return response.json()
