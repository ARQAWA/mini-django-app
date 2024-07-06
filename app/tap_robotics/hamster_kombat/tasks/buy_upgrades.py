from typing import cast

from httpx import HTTPStatusError
from loguru import logger

from app.core.clients.tma_hamster import TMAHamsterKombat
from app.core.common.executors import syncp
from app.tap_robotics.hamster_kombat.common.queue import task_queue
from app.tap_robotics.hamster_kombat.common.wrapper import FailResult, wrap_http_request
from app.tap_robotics.hamster_kombat.dicts.clicker_upgrade import ClickerDailyComboDict, ClickerUpgradeDict
from app.tap_robotics.hamster_kombat.dicts.clicker_user import ClickerUserDict
from app.tap_robotics.hamster_kombat.isolated.get_most_profitable_upgrade import get_most_profitable_upgrades
from app.tap_robotics.hamster_kombat.schemas import HamsterTask


async def buy_upgrades_hamster_kombat(task: HamsterTask) -> None:
    """Задача на покупку апгрейдов."""
    client = TMAHamsterKombat()

    if task.user is None:
        logger.error(f"User is None for account {task.account_id}")
        return

    result = await wrap_http_request(
        client.get_upgrades_list(task.auth_token, task.user_agent),
        task.account_id,
        f"Failed to get upgrades list for account {task.account_id}",
    )

    if isinstance(result, (FailResult, HTTPStatusError)):
        return

    upgrades, _ = cast(tuple[list[ClickerUpgradeDict], ClickerDailyComboDict], result)  # noqa: F841
    user, errors, success, pphd = await buy_upgrades(upgrades, task)
    success += 1

    logger.debug(f"Synced account {task.account_id} / Balance: {user["balanceCoins"]}")
    await task_queue.put(
        task.next(
            action="finish",
            user=user,
            stats_dict={"cards": success - 1, "pphd": pphd},
            net_success=success,
            net_errors=errors,
        )
    )


async def buy_upgrades(
    upgrades: list[ClickerUpgradeDict],
    task: HamsterTask,
) -> tuple[ClickerUserDict, dict[str, int], int, int]:
    """Buy upgrades."""
    client = TMAHamsterKombat()

    pphd = 0
    success = 0
    errors: dict[str, int] = {}
    user = cast(ClickerUserDict, task.user)
    while True:
        upgrades = cast(list[ClickerUpgradeDict], await syncp(get_most_profitable_upgrades)(upgrades, 15))
        for upgrade in upgrades:
            if user["balanceCoins"] < upgrade["price"]:
                continue

            result = await wrap_http_request(
                client.buy_upgrade(task.auth_token, task.user_agent, upgrade["id"]),
                task.account_id,
                f"Failed to buy upgrade {upgrade["id"]} for account {task.account_id}",
            )

            if isinstance(result, FailResult):
                return user, errors, success, pphd

            if isinstance(result, HTTPStatusError):
                code_str = str(result.response.status_code)
                errors[code_str] = errors.get(code_str, 0) + 1
                return user, errors, success, pphd

            success += 1
            pphd += upgrade["profitPerHourDelta"]
            user, upgrades, _ = cast(  # noqa: F841
                tuple[ClickerUserDict, list[ClickerUpgradeDict], ClickerDailyComboDict],
                result,
            )
            break
        else:
            break

    return user, errors, success, pphd
