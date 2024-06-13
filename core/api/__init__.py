from ninja import NinjaAPI, Router

from core.api.v1 import router as v1_router
from core.renderers import ORJSONResponseRenderer

router = Router()
router.add_router("/v1/", v1_router)

api = NinjaAPI(
    title="Mini Django App",
    version="0.0.1",
    description="A mini Django app to research Telegram Mini Apps",
    renderer=ORJSONResponseRenderer(),
    default_router=router,
)
