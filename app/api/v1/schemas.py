from ninja import Schema
from pydantic import Field


class MePostBody(Schema):
    """Схема тела запроса."""

    init_data: str = Field(alias="initData", description="Инициализационные данные")

    # @property
    # def init_object(self) -> dict[str, Any]:
    #     """Свойство для возврата объекта."""
    #     if not self.init_data:
    #         return {}
    #
    #     res = orjson.loads(self.init_data)
    #
    #     if not isinstance(res, dict):
    #         raise ValueError("initData must be a dictionary")
    #
    #     return res
