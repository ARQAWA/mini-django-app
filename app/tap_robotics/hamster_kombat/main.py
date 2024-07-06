import asyncio
from datetime import timedelta
from typing import Generator, cast

from django.db.models import Q
from django.db.models.functions import Now
from loguru import logger

from app.core.apps.core.models import Game
from app.core.apps.games.models import Account, Session
from app.core.common.executors import synct
from app.core.libs.httpx_ import get_proxy_client
from app.tap_robotics.hamster_kombat.common.queue import task_queue
from app.tap_robotics.hamster_kombat.executor import task_executor
from app.tap_robotics.hamster_kombat.schemas import AccInfo, HamsterTask

AccsResult = tuple[Generator[AccInfo, None, None], int]


async def run_hamster() -> None:
    """Функция запуска бота."""
    [asyncio.create_task(task_executor()) for _ in range(100)]

    while True:
        accs, count = cast(AccsResult, await synct(get_players)())
        logger.debug(f"Found {count} accounts to play")
        if count:
            await asyncio.gather(*(run_account(acc) for acc in accs))
        await asyncio.sleep(7)


def get_players() -> AccsResult:
    """Получение аккаунтов, которые могут играть."""
    accs = (
        Account.objects.filter(
            Q(game_id=Game.LITERAL_HAMSTER_KOMBAT),
            Q(is_playing=True),
            Q(slot__payment__is_payed=True, slot__expired_at__gt=Now()),
            Q(session__isnull=True) | Q(session__next_at__lte=Now()),
        )
        .only("auth_token", "user_agent", "proxy_url")
        .distinct()
    )

    return (
        {
            "id": acc.id,
            "auth_token": acc.auth_token,
            "user_agent": acc.user_agent,
            "proxy": acc.proxy_url,
        }
        for acc in accs
    ), accs.count()


async def run_account(acc: AccInfo) -> None:
    """Запуск аккаунта."""
    await Session.objects.aupdate_or_create(
        account_id=acc["id"],
        defaults={"errors": 0, "next_at": Now() + timedelta(minutes=60)},
    )

    await task_queue.put(
        HamsterTask(
            account_id=acc["id"],
            auth_token=acc["auth_token"],
            user_agent=acc["user_agent"],
            proxy_client=None if acc["proxy"] is None else get_proxy_client(acc["proxy"]),
            action="sync",
        )
    )
