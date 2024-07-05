import asyncio
from functools import partial

from httpx import HTTPStatusError
from loguru import logger

from app.core.apps.core.models import Game
from app.core.clients.tma_hamster import TMAHamsterKombat
from app.core.common.executors import synct
from app.core.libs.redis_ import redis_client
from app.core.services.network_stats import write_network_stats
from app.tap_robotics.hamster_kombat.common import task_queue
from app.tap_robotics.hamster_kombat.schemas import HamsterTask


async def execute_tasks_hamster_kombat(task: HamsterTask) -> None:
    """Задача на выполнение задач."""
    check_key = f"{Game.LITERAL_HAMSTER_KOMBAT}:execute_tasks:{task.account_id}"

    if await redis_client.exists(check_key):
        return

    client = TMAHamsterKombat()

    if task.user is None:
        logger.error(f"User is None for account {task.account_id}")
        return

    try:
        tasks = await client.get_tasks(task.auth_token, task.user_agent)
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

    if not tasks:
        logger.debug(f"User {task.account_id} has no tasks")
        await task_queue.put(task.next(action="buy_upgrades", net_success=1))
        redis_checkout_tasks(check_key)
        return

    user = task.user
    task_erros = {}
    success = 1
    for task_ in tasks:
        try:
            user = await client.complete_task(task.auth_token, task.user_agent, task_["id"])
            success += 1
        except HTTPStatusError as err:
            logger.error(f"Failed to sync account {task.account_id}: {err}")
            if (err_str := str(err.response.status_code)) in task_erros:
                task_erros[err_str] = 0
            task_erros[err_str] += 1
            continue
        except Exception as err:
            logger.error(f"Failed to sync account {task.account_id}: {err}")
            continue

    redis_checkout_tasks(check_key)
    logger.debug(f"Synced account {task.account_id} / Balance: {user["balanceCoins"]}")
    await task_queue.put(
        task.next(
            action="buy_upgrades",
            user=user,
            net_success=success,
        )
    )


def redis_checkout_tasks(check_key: str) -> None:
    """Checkout tasks."""
    asyncio.create_task(redis_client.set(check_key, 1, ex=7500))  # type: ignore
