import time

from hamster.client import hamster_client
from hamster.schemas.upgrades_for_buy import Upgrade


def print_exit(message: str, *, timer: float = 10) -> None:
    """Print a message and exit after 10 seconds."""
    print(message)  # noqa
    time.sleep(timer)
    exit()


mpf_upgrade: Upgrade | None = None


def get_mpf_upgrade() -> None:
    """Get the most profitable upgrade."""
    global mpf_upgrade

    # 3. Fetch upgrades list
    upgrades_list = hamster_client.get_upgrades_list()
    if upgrades_list is None:
        return print_exit("Failed to fetch upgrades list.")

    if not upgrades_list.upgrades_for_buy:
        return print_exit("No upgrades available.")

    # 4. Get the most profitable upgrade
    mpf_upgrade = upgrades_list.get_most_profitable_upgrade(user_data.balance_coins)  # type: ignore


def buy_upgrade_by_id() -> None:
    """Buy the most profitable upgrade."""
    global user_data

    if mpf_upgrade is None:
        return print_exit("No upgrade available.")

    # 5. Buy the most profitable upgrade
    user_data = hamster_client.buy_upgrade(mpf_upgrade)
    if user_data is None:
        return print_exit("Failed to buy upgrade.")

    get_mpf_upgrade()


# 1. Fetch user data
user_data = hamster_client.sync()
if user_data is None:
    print_exit("Failed to fetch user data.")
    exit()

# 2. Tap the hamster
user_data = hamster_client.taps(user_data)

get_mpf_upgrade()
while True:
    if mpf_upgrade is None:
        break

    if user_data.balance_coins >= mpf_upgrade.price:
        buy_upgrade_by_id()
    else:
        print(f"Want to upgrade {mpf_upgrade.id}; COST: {mpf_upgrade.price:,}; PROFIT: {mpf_upgrade.profit_per_hour:,}")  # noqa
        print("Insufficient balance.")  # noqa

        seconds_to_upgrade = (mpf_upgrade.price - user_data.balance_coins) / user_data.earn_passive_per_sec
        seconds_to_recover = (user_data.max_taps - user_data.available_taps) / user_data.taps_recover_per_sec

        sleep_time = min(seconds_to_upgrade, seconds_to_recover)
        if sleep_time <= 0:
            sleep_time = 10.0

        if sleep_time > 600.0:
            sleep_time = 600.0

        print(f"Sleeping for {sleep_time:,.0f} seconds.")  # noqa
        print_exit(f"Balance: {user_data.balance_coins:,.0f}, Price: {mpf_upgrade.price:,}", timer=sleep_time)  # noqa
