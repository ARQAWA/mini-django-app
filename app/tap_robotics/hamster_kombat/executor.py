from loguru import logger

from app.tap_robotics.hamster_kombat.common import task_queue
from app.tap_robotics.hamster_kombat.tasks.sync import sync_hamster_kombat
from app.tap_robotics.hamster_kombat.tasks.tap_hamster import tap_hamster_hamster_kombat


async def task_executor() -> None:
    """Воркер для выполнения задач."""
    while True:
        task = await task_queue.get()

        match task.action:
            case "sync":
                logger.debug(f"Syncing account {task.account_id}")
                await sync_hamster_kombat(task)
            case "tap_hamster":
                logger.debug(f"Tapping hamster for account {task.account_id}")
                await tap_hamster_hamster_kombat(task)
            case _:
                logger.debug(f"Unknown action {task.action} for account {task.account_id}")
