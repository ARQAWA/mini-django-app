import random
import time

from hamster.client import hamster_client

LAST_SYNC = 0.0


def print_exit(message: str, *, timer: float = 10.0) -> None:
    """Print a message and exit after 10 seconds."""
    print(message)  # noqa
    print(f"Going to sleep for {timer} seconds.")  # noqa
    time.sleep(timer)


def run() -> None:  # noqa: C901
    """Run the hamster clicker."""
    global LAST_SYNC

    # 1. Fetch user data
    user_data = hamster_client.sync()
    if user_data is None:
        return print_exit("Failed to fetch user data.")

    if (cur_sync := time.time()) > LAST_SYNC + 300:
        LAST_SYNC = cur_sync

        # 2. Tap the hamster
        user_data = hamster_client.taps(user_data)

    while True:
        bought_upgrade = False

        # 3. Fetch upgrades list
        upgrades_list = hamster_client.get_upgrades_list()
        if upgrades_list is None:
            return print_exit("Failed to fetch upgrades list.")

        if not upgrades_list.daily_combo.is_claimed and len(upgrades_list.daily_combo.upgrade_ids) == 3:
            user_data = hamster_client.claim_combo()
            if user_data is None:
                return print_exit("Failed to claim combo.")

        if not upgrades_list.upgrades_for_buy:
            return print_exit("No upgrades available.")

        # 4. Buy upgrades
        mfp_upgrades = upgrades_list.get_most_profitable_upgrades()
        for i, mpf_upgrade in enumerate(mfp_upgrades):
            if i >= 10:
                if not bought_upgrade:
                    return print_exit("No upgrades available.", timer=180.0)
                break

            if user_data.balance_coins < mpf_upgrade.price:
                continue

            user_data = hamster_client.buy_upgrade(mpf_upgrade)
            if user_data is None:
                return print_exit("Failed to buy upgrade.")

            bought_upgrade = True

            time.sleep(random.randint(0, 5))


while True:
    run()
