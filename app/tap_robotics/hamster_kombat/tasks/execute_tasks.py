import asyncio
from typing import cast

from httpx import HTTPStatusError
from loguru import logger

from app.core.apps.core.models import Game
from app.core.clients.tma_hamster import TMAHamsterKombat
from app.core.libs.redis_ import redis_client
from app.tap_robotics.hamster_kombat.common.queue import task_queue
from app.tap_robotics.hamster_kombat.common.wrapper import FailResult, wrap_http_request
from app.tap_robotics.hamster_kombat.dicts.clicker_tasks import ClickerTaskDict
from app.tap_robotics.hamster_kombat.dicts.clicker_user import ClickerUserDict
from app.tap_robotics.hamster_kombat.schemas import HamsterTask


async def execute_tasks_hamster_kombat(task: HamsterTask) -> None:
    """Задача на выполнение задач."""
    check_key = f"{Game.LITERAL_HAMSTER_KOMBAT}:execute_tasks:{task.account_id}"

    if (await redis_client.get(check_key)) is not None:
        logger.debug(f"Tasks for account {task.account_id} are already executed")
        await task_queue.put(task.next(action="buy_upgrades"))
        return

    client = TMAHamsterKombat()

    if task.user is None:
        logger.error(f"User is None for account {task.account_id}")
        return

    result = await wrap_http_request(
        client.get_tasks(task.auth_token, task.user_agent, task.proxy_client),
        task.account_id,
        f"Failed to get tasks for account {task.account_id}",
    )

    if isinstance(result, (FailResult, HTTPStatusError)):
        return

    tasks = cast(list[ClickerTaskDict], result)
    if not tasks:
        logger.debug(f"User {task.account_id} has no tasks")
        await task_queue.put(task.next(action="buy_upgrades", net_success=1))
        redis_checkout_tasks(check_key)
        return

    user = task.user
    task_erros = {}
    success = 1

    for task_ in tasks:
        if task_["isCompleted"]:
            continue

        result_ = await wrap_http_request(
            client.complete_task(task.auth_token, task.user_agent, task.proxy_client, task_["id"]),
            task.account_id,
            f"Failed to complete task {task_["id"]} for account {task.account_id}",
            False,
        )

        if isinstance(result_, FailResult):
            continue

        if isinstance(result_, HTTPStatusError):
            if (err_str := str(result_.response.status_code)) in task_erros:
                task_erros[err_str] = 0
            task_erros[err_str] += 1
            continue

        user = cast(ClickerUserDict, result_)

    redis_checkout_tasks(check_key)
    logger.debug(f"Synced account {task.account_id} / Balance: {user["balanceCoins"]}")
    await task_queue.put(
        task.next(
            action="buy_upgrades",
            user=user,
            stats_dict={"tasks": success - 1},
            net_success=success,
            net_errors=task_erros,
        )
    )


def redis_checkout_tasks(check_key: str) -> None:
    """Checkout tasks."""
    asyncio.create_task(redis_client.set(check_key, 1, ex=7500))  # type: ignore
