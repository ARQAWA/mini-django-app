import time

from httpx import Client

from app.core.envs import envs
from hamster.schemas.clicker_user import ClickerUser
from hamster.schemas.upgrades_for_buy import Upgrade, UpgradesData


class HamsterClient:
    """HTTP client for the Hamster API."""

    _headers = {
        "Authorization": "Bearer " + envs.hamster.token,
        "Origin": "https://hamsterkombat.io",
        "Referer": "https://hamsterkombat.io/",
        "User-Agent": envs.hamster.user_agent,
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
    }

    def __init__(self) -> None:
        self._http = Client(headers=self._headers)

    def sync(self) -> ClickerUser | None:
        """Sync the user's data."""
        print(f"Syncing user data...")  # noqa

        response = self._http.post("https://api.hamsterkombat.io/clicker/sync")

        try:
            jresponse = response.json()["clickerUser"]
        except Exception as err:
            print(err, response.status_code, response.text[:32])  # noqa
            return None

        return ClickerUser.model_validate(jresponse)

    def taps(self, clicker: ClickerUser) -> ClickerUser:
        """Tap the hamster."""
        print(f"Tapping the hamster...")  # noqa

        available_taps = clicker.available_taps

        extra_taps = int((time.time() - clicker.sync_time) * clicker.taps_recover_per_sec)

        if extra_taps > 0:
            available_taps += extra_taps

        if available_taps > clicker.max_taps:
            available_taps = clicker.max_taps

        count = available_taps // clicker.earn_per_tap

        response = self._http.post(
            "https://api.hamsterkombat.io/clicker/tap",
            json={
                "count": count,
                "availableTaps": available_taps,
                "timestamp": int(time.time()),
            },
        )

        try:
            jresponse = response.json()["clickerUser"]
        except Exception as err:
            print(err, response.status_code, response.text[:32])  # noqa
            return clicker

        return ClickerUser.model_validate(jresponse)

    def get_upgrades_list(self) -> UpgradesData | None:
        """Get the list of upgrades."""
        print(f"Fetching upgrades list...")  # noqa

        response = self._http.post("https://api.hamsterkombat.io/clicker/upgrades-for-buy")

        try:
            jresponse = response.json()
        except Exception as err:
            print(err, response.status_code, response.text[:32])  # noqa
            return None

        return UpgradesData.model_validate(jresponse)

    def buy_upgrade(self, upgrade: Upgrade) -> ClickerUser | None:
        """Buy an upgrade."""
        print(f"Buying upgrade {upgrade.id}; COST: {upgrade.price:,}; PROFIT: {upgrade.profit_per_hour:,}")  # noqa

        response = self._http.post(
            "https://api.hamsterkombat.io/clicker/buy-upgrade",
            json={
                "upgradeId": upgrade.id,
                "timestamp": int(time.time()),
            },
        )

        try:
            jresponse = response.json()["clickerUser"]
        except Exception as err:
            print(err, response.status_code, response.text[:32])  # noqa
            return None

        return ClickerUser.model_validate(jresponse)


hamster_client = HamsterClient()
