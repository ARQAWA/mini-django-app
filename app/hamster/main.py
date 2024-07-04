import time

import sentry_sdk
from loguru import logger

from app.hamster.client import hamster_client


class TIMERS:
    """The timers for the hamster clicker."""

    DAILY = 0


def print_exit(message: str, *, timer: float = 10.0) -> None:
    """logger.debug a message and exit after 10 seconds."""
    logger.debug(message)
    logger.debug(f"Going to sleep for {timer} seconds.")
    time.sleep(timer)


def run() -> None:  # noqa: C901
    """Run the hamster clicker."""
    # 1. Fetch user data
    user_data = hamster_client.sync()
    if user_data is None:
        return print_exit("Failed to fetch user data.")

    # 2. Tap the hamster
    user_data = hamster_client.taps(user_data)

    # Fetch tasks
    if time.time() >= TIMERS.DAILY:
        tasks = hamster_client.get_tasks()
        for task in tasks:
            if task["isCompleted"]:
                continue
            user_data = hamster_client.pick_task(task["id"])
            if user_data is None:
                return print_exit("Failed to pick task.")
        TIMERS.DAILY = time.time() + 60 * 60 * 3  # 3 hours

    # 3. Fetch upgrades list
    upgrades_list = hamster_client.get_upgrades_list()
    if upgrades_list is None:
        return print_exit("Failed to fetch upgrades list.")

    # 4. Buy upgrades
    while True:
        # 5. Claim daily combo
        if upgrades_list.can_claim_combo:
            claim_result = hamster_client.claim_combo()
            if claim_result is None:
                return print_exit("Failed to claim combo.")
            user_data, _ = claim_result  # noqa: F841

        # 6. Buy most profitable upgrades
        mfp_upgrades = upgrades_list.get_most_profitable_upgrades()
        for i, mpf_upgrade in enumerate(mfp_upgrades):
            if i >= 10:
                return print_exit("No upgrades available.", timer=180.0)

            if user_data.balance_coins < mpf_upgrade.price:
                continue

            buy_result = hamster_client.buy_upgrade(mpf_upgrade)
            if buy_result is None:
                return print_exit("Failed to buy upgrade.")

            user_data, upgrades_list = buy_result
            break


if __name__ == "__main__":
    from asyncio import CancelledError
    from contextlib import suppress

    from app.core.common.sentry import sentry_init

    try:
        with suppress(KeyboardInterrupt, SystemExit, CancelledError):
            sentry_init()
            while True:
                try:
                    run()
                except Exception as err:
                    logger.error(err)
                    sentry_sdk.capture_exception(err)
                    time.sleep(15.0)
    finally:
        hamster_client.close()
