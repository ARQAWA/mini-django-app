from ninja import Router

from core.api.v1.me import router as me_router

router = Router()
router.add_router("", me_router)
