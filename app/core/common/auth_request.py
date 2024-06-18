from django.http import HttpRequest as DjangoHttpRequest

from app.core.models.tg_user_data import PlayerData


class HttpRequest(DjangoHttpRequest):
    """Класс для запроса с объектом авторизации."""

    auth: PlayerData.Dict
