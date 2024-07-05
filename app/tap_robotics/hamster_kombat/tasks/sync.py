from functools import partial

from httpx import HTTPStatusError
from loguru import logger

from app.core.clients.tma_hamster import TMAHamsterKombat
from app.core.common.executors import synct
from app.core.services.network_stats import write_network_stats
from app.tap_robotics.hamster_kombat.common import task_queue
from app.tap_robotics.hamster_kombat.schemas import HamsterTask


async def sync_hamster_kombat(task: HamsterTask) -> None:
    """Синхронизировать данные пользователя в TMA Hamster Kombat."""
    client = TMAHamsterKombat()

    try:
        user = await client.sync(task.auth_token, task.user_agent)
    except HTTPStatusError as err:
        logger.error(f"Failed to sync account {task.account_id}: {err}")
        func_write = partial(
            write_network_stats,
            account_id=task.account_id,
            success=0,
            error_code={str(err.response.status_code): 1},
        )
        await synct(func_write)()
        return
    except Exception as err:
        logger.error(f"Failed to sync account {task.account_id}: {err}")
        return

    logger.info(f"Synced account {task.account_id} / Balance: {user["balanceCoins"]}")
    await task_queue.put(
        task.next(
            action="tap_hamster",
            user=user,
            net_success=1,
        )
    )
