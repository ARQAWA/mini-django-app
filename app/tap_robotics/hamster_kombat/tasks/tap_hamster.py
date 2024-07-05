from typing import cast

from httpx import HTTPStatusError
from loguru import logger

from app.core.clients.tma_hamster import TMAHamsterKombat
from app.core.common.executors import syncp
from app.tap_robotics.hamster_kombat.common.queue import task_queue
from app.tap_robotics.hamster_kombat.common.wrapper import FailResult, wrap_http_request
from app.tap_robotics.hamster_kombat.dicts.clicker_user import ClickerUserDict
from app.tap_robotics.hamster_kombat.isolated.get_taps import get_available_taps
from app.tap_robotics.hamster_kombat.schemas import HamsterTask


async def tap_hamster_hamster_kombat(task: HamsterTask) -> None:
    """Задача для тапа хомяка."""
    client = TMAHamsterKombat()

    if task.user is None:
        logger.error(f"User is None for account {task.account_id}")
        return

    count, available_taps = cast(tuple[int, int], await syncp(get_available_taps)(task.user))

    if not count:
        logger.debug(f"User {task.account_id} has no available taps")
        await task_queue.put(
            task.next(
                action="execute_tasks",
            )
        )
        return

    result = await wrap_http_request(
        client.tap_hamster(task.auth_token, task.user_agent, count, available_taps),
        task.account_id,
        f"Failed to tap account {task.account_id}",
    )

    if isinstance(result, (FailResult, HTTPStatusError)):
        return

    user = cast(ClickerUserDict, result)
    logger.debug(f"Synced account {task.account_id} / Balance: {user["balanceCoins"]}")
    await task_queue.put(
        task.next(
            action="execute_tasks",
            user=user,
            net_success=1,
        )
    )
