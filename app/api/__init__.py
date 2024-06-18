from ninja import NinjaAPI

from app.api.router import router as root_router
from app.core.exceptions import setup_exception_handlers
from app.core.renderers import ORJSONResponseRenderer


def init_api() -> NinjaAPI:
    """Инициализация API."""
    api = NinjaAPI(
        title="Mini Django App",
        version="0.0.1",
        description="A mini Django app to research Telegram Mini Apps",
        renderer=ORJSONResponseRenderer(),
        default_router=root_router,
    )
    setup_exception_handlers(api)

    return api
