import time
from typing import cast

from httpx import Client
from loguru import logger

from app.core.envs import envs
from app.hamster.schemas.clicker_user import ClickerUser, Task
from app.hamster.schemas.upgrades_for_buy import DailyCombo, Upgrade, UpgradesData


class HamsterClient:
    """HTTP client for the Hamster API."""

    def __init__(self) -> None:
        if envs.hamster is None:
            raise RuntimeError("Hamster API is not configured")

        self._headers = {
            "Authorization": "Bearer " + envs.hamster.token,
            "Origin": "https://hamsterkombat.io",
            "Referer": "https://hamsterkombat.io/",
            "User-Agent": envs.hamster.user_agent,
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
        }
        self._http = Client(headers=self._headers)

    def close(self) -> None:
        """Close the HTTP client."""
        self._http.close()

    def sync(self) -> ClickerUser | None:
        """Sync the user's data."""
        logger.debug("Syncing user data...")

        response = self._http.post("https://api.hamsterkombat.io/clicker/sync")

        try:
            jresponse = response.json()["clickerUser"]
        except Exception as err:
            logger.debug((err, response.status_code, response.text[:32]))
            return None

        return ClickerUser.model_validate(jresponse)

    def taps(self, clicker: ClickerUser) -> ClickerUser:
        """Tap the hamster."""
        logger.debug("Tapping the hamster...")

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
            logger.debug((err, response.status_code, response.text[:32]))
            return clicker

        return ClickerUser.model_validate(jresponse)

    def get_upgrades_list(self) -> UpgradesData | None:
        """Get the list of upgrades."""
        logger.debug("Fetching upgrades list...")

        response = self._http.post("https://api.hamsterkombat.io/clicker/upgrades-for-buy")

        try:
            jresponse = response.json()
        except Exception as err:
            logger.debug((err, response.status_code, response.text[:32]))
            return None

        return UpgradesData.model_validate(jresponse)

    def buy_upgrade(self, upgrade: Upgrade) -> tuple[ClickerUser, UpgradesData] | None:
        """Buy an upgrade."""
        logger.debug(
            f"Buying upgrade {upgrade.id}; LEVEL: {upgrade.level}; "
            f"COST: {upgrade.price:,}; PROFIT: {upgrade.profit_per_hour:,}"
        )

        response = self._http.post(
            "https://api.hamsterkombat.io/clicker/buy-upgrade",
            json={
                "upgradeId": upgrade.id,
                "timestamp": int(time.time()),
            },
        )

        try:
            jresponse = response.json()
        except Exception as err:
            logger.debug((err, response.status_code, response.text[:32]))
            return None

        clicker = ClickerUser.model_validate(jresponse["clickerUser"])
        upgrades = UpgradesData.model_validate(jresponse)
        return clicker, upgrades

    def claim_combo(self) -> tuple[ClickerUser, DailyCombo] | None:
        """Claim combo."""
        logger.debug("Claiming daily combo...")

        response = self._http.post("https://api.hamsterkombat.io/clicker/claim-daily-combo")

        try:
            jresponse = response.json()
        except Exception as err:
            logger.debug((err, response.status_code, response.text[:32]))
            return None

        clicker = ClickerUser.model_validate(jresponse["clickerUser"])
        daily_combo = DailyCombo.model_validate(jresponse["dailyCombo"])
        return clicker, daily_combo

    def get_tasks(self) -> list[Task]:
        """Get tasks."""
        logger.debug("Fetching tasks...")

        response = self._http.post("https://api.hamsterkombat.io/clicker/list-tasks")

        try:
            jresponse = cast(dict[str, list[Task]], response.json())
        except Exception as err:
            logger.debug((err, response.status_code, response.text[:32]))
            return []

        return jresponse["tasks"]

    def pick_task(self, task_id: str) -> ClickerUser | None:
        """Pick a task."""
        logger.debug(f"Picking task {task_id}...")

        response = self._http.post(
            "https://api.hamsterkombat.io/clicker/check-task",
            json={"taskId": task_id},
        )

        try:
            jresponse = response.json()
        except Exception as err:
            logger.debug((err, response.status_code, response.text[:32]))
            return None

        return ClickerUser.model_validate(jresponse["clickerUser"])


hamster_client = HamsterClient()
