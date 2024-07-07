from typing import TypedDict


class ClickerUpgradeConditionDict(TypedDict):
    """Clicker upgrade condition dict."""

    _type: str
    upgradeId: str
    level: int


class ClickerUpgradeDict(TypedDict):
    """Clicker upgrade dict."""

    id: str
    level: int
    price: int
    profitPerHourDelta: int
    isExpired: bool
    isAvailable: bool
    cooldownSeconds: int | None
    condition: ClickerUpgradeConditionDict | None


class ClickerDailyComboDict(TypedDict):
    """Clicker daily combo dict."""

    upgradeIds: list[str]
    isClaimed: bool
