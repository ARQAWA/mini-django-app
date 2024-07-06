from typing import cast

from httpx import HTTPStatusError
from loguru import logger

from app.core.clients.tma_hamster import TMAHamsterKombat
from app.tap_robotics.hamster_kombat.common.queue import task_queue
from app.tap_robotics.hamster_kombat.common.wrapper import FailResult, wrap_http_request
from app.tap_robotics.hamster_kombat.dicts.clicker_user import ClickerUserDict
from app.tap_robotics.hamster_kombat.schemas import HamsterTask


async def sync_hamster_kombat(task: HamsterTask) -> None:
    """Синхронизировать данные пользователя в TMA Hamster Kombat."""
    client = TMAHamsterKombat()

    result = await wrap_http_request(
        client.sync(task.auth_token, task.user_agent, task.proxy_client),
        task.account_id,
        f"Failed to sync account {task.account_id}",
    )

    if isinstance(result, (FailResult, HTTPStatusError)):
        return

    user = cast(ClickerUserDict, result)
    logger.debug(f"Synced account {task.account_id} / Balance: {user["balanceCoins"]}")
    await task_queue.put(
        task.next(
            action="tap_hamster",
            user=user,
            net_success=1,
        )
    )
