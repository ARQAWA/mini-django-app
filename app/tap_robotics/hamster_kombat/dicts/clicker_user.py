from typing import TypedDict


class ClickerUserDict(TypedDict):
    """Clicker user dict."""

    totalCoins: float
    balanceCoins: float
    availableTaps: int
    maxTaps: int
    earnPerTap: int
    earnPassivePerSec: float
    earnPassivePerHour: int
    lastPassiveEarn: float
    tapsRecoverPerSec: int
