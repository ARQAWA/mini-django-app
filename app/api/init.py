from ninja import NinjaAPI

from app.api.router import router as root_router
from app.core.common.ninjas_fix.exceptions import setup_exception_handlers
from app.core.common.ninjas_fix.renderers import ORJSONResponseRenderer


def init_api() -> NinjaAPI:
    """Инициализация API."""
    api = NinjaAPI(
        title="Mini Django App",
        version="0.0.1",
        description="A mini Django app to research Telegram Mini Apps",
        openapi_url="/top-secret-x-files-1337-322-228-666/openapi.json",
        docs_url="/our-awesome-api-docs-1337-322-228-666/",
        renderer=ORJSONResponseRenderer(),
        default_router=root_router,
    )
    setup_exception_handlers(api)

    return api
