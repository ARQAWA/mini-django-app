from functools import partial

from loguru import logger

from app.core.common.executors import synct
from app.core.services.network_stats import write_network_stats
from app.tap_robotics.hamster_kombat.schemas import HamsterTask
from app.tap_robotics.hamster_kombat.stats.play import write_play_stats


async def finish_hamster_kombat(task: HamsterTask) -> None:
    """Синхронизировать данные пользователя в TMA Hamster Kombat."""
    if task.user is None:
        logger.error(f"User is None for account {task.account_id}")
        return

    await synct(
        partial(
            write_network_stats,
            account_id=task.account_id,
            success=task.net_success,
            error_code=task.net_errors,
        )
    )()

    await synct(
        partial(
            write_play_stats,
            account_id=task.account_id,
            balance=int(task.user["balanceCoins"]),
            pph=task.user["earnPassivePerHour"],
            **task.stats_dict,
        )
    )()

    logger.debug(f"Finished account {task.account_id}")
