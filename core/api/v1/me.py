import asyncio
import random
import time

from django.http import HttpRequest
from ninja import Router

router = Router(tags=["auth"])


@router.get(
    "/me",
    summary="Информация о текущем пользователе",
    description="Ручка для получения информации о текущем пользователе.",
    response={200: str},
)
async def me(request: HttpRequest) -> str:
    """Ручка для получения информации о текущем пользователе."""
    t_start = time.time()
    print(f"Start: {t_start:.2f} sec {hash(request)}")  # noqa

    await asyncio.sleep(random.randint(1, 3))

    t_end = time.time()
    print(f"End: {t_end:.2f} sec {hash(request)}")  # noqa

    t_sum = t_end - t_start

    return f"Hello World! {t_sum:.2f}"
