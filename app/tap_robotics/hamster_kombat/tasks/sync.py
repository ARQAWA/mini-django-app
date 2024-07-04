from httpx import HTTPStatusError
from loguru import logger

from app.core.clients.tma_hamster import TMAHamsterKombat
from app.tap_robotics.hamster_kombat.common import task_queue
from app.tap_robotics.hamster_kombat.schemas import HamsterTask


async def sync_hamster_kombat(task: HamsterTask) -> None:
    """Синхронизировать данные пользователя в TMA Hamster Kombat."""
    client = TMAHamsterKombat()

    try:
        user = await client.sync(task.auth_token, task.user_agent)
    except HTTPStatusError as err:
        logger.error(f"Failed to sync account {task.account_id}: {err}")
        # write network error to db
        return
    except Exception as err:
        logger.error(f"Failed to sync account {task.account_id}: {err}")
        return

    # write user stats to db
    logger.info(f"Synced account {task.account_id}: {user}")
    await task_queue.put(task.next(action="tap_hamster", user=user))
