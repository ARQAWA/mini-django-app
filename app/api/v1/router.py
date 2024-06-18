from ninja import Router

from app.api.v1.user.router import router as user_router
from app.core.common.auth_dep import player_auth

router = Router(auth=player_auth)
router.add_router("/user/", user_router)
