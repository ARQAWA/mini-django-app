from loguru import logger

from app.tap_robotics.hamster_kombat.common.queue import task_queue
from app.tap_robotics.hamster_kombat.tasks.buy_upgrades import buy_upgrades_hamster_kombat
from app.tap_robotics.hamster_kombat.tasks.execute_tasks import execute_tasks_hamster_kombat
from app.tap_robotics.hamster_kombat.tasks.finish import finish_hamster_kombat
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
            case "execute_tasks":
                logger.debug(f"Checking tasks for account {task.account_id}")
                await execute_tasks_hamster_kombat(task)
            case "buy_upgrades":
                logger.debug(f"Buying upgrades for account {task.account_id}")
                await buy_upgrades_hamster_kombat(task)
            case "finish":
                logger.debug(f"Finishing account {task.account_id}")
                await finish_hamster_kombat(task)
