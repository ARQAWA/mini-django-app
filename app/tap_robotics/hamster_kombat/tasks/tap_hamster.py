

from app.core.clients.tma_hamster import TMAHamsterKombat
from app.tap_robotics.hamster_kombat.schemas import HamsterTask


async def tap_hamster_hamster_kombat(task: HamsterTask) -> None:
    """Задача для тапа хомяка."""
    TMAHamsterKombat()

    # try:
    #     user = await client.sync(task.auth_token, task.user_agent)
    # except HTTPStatusError as err:
    #     logger.error(f"Failed to sync account {task.account_id}: {err}")
    #     func_write = partial(
    #         write_network_stats,
    #         account_id=task.account_id,
    #         success=0,
    #         error_code={str(err.response.status_code): 1},
    #     )
    #     await synct(func_write)()
    #     return
    # except Exception as err:
    #     logger.error(f"Failed to sync account {task.account_id}: {err}")
    #     return
    #
    # if user is None:
    #     logger.error(f"Failed to sync account {task.account_id}: User is None")
    #     return
    #
    # logger.info(f"Synced account {task.account_id} / Balance: {user["balanceCoins"]}")
    # await task_queue.put(
    #     task.next(
    #         action="tap_hamster",
    #         user=user,
    #     )
    # )
