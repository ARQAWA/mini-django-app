from functools import partial
from typing import cast

from httpx import HTTPStatusError
from loguru import logger

from app.core.clients.tma_hamster import TMAHamsterKombat
from app.core.common.executors import syncp, synct
from app.core.services.network_stats import write_network_stats
from app.tap_robotics.hamster_kombat.common import task_queue
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

    try:
        user = await client.tap_hamster(task.auth_token, task.user_agent, count, available_taps)
    except HTTPStatusError as err:
        logger.error(f"Failed to sync account {task.account_id}: {err}")
        await synct(
            partial(
                write_network_stats,
                account_id=task.account_id,
                success=0,
                error_code={str(err.response.status_code): 1},
            )
        )()
        return
    except Exception as err:
        logger.error(f"Failed to sync account {task.account_id}: {err}")
        return

    logger.debug(f"Synced account {task.account_id} / Balance: {user["balanceCoins"]}")
    await task_queue.put(
        task.next(
            action="execute_tasks",
            user=user,
            net_success=1,
        )
    )
