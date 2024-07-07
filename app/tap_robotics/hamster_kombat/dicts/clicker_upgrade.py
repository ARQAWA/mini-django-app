from typing import TypedDict


class ClickerUpgradeDict(TypedDict):
    """Clicker upgrade dict."""

    id: str
    level: int
    price: int
    profitPerHourDelta: int
    isExpired: bool
    isAvailable: bool
    cooldownSeconds: int | None


class ClickerDailyComboDict(TypedDict):
    """Clicker daily combo dict."""

    upgradeIds: list[str]
    isClaimed: bool
