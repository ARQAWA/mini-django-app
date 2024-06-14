from ninja import Router

from app.api.v1.router import router as v1_router

router = Router()
router.add_router("/v1/", v1_router)
