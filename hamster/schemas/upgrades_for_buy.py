from decimal import Decimal
from typing import List, Optional

import numpy
from pydantic import BaseModel, ConfigDict, Field, computed_field


class Condition(BaseModel):
    """The condition object."""

    type: str = Field(..., alias="_type")
    upgrade_id: Optional[str] = Field(None, alias="upgradeId")
    level: Optional[int] = None
    referral_count: Optional[int] = Field(None, alias="referralCount")
    more_referrals_count: Optional[int] = Field(None, alias="moreReferralsCount")
    subscribe_link: Optional[str] = Field(None, alias="subscribeLink")
    links: Optional[List[str]] = None
    channel_id: Optional[int] = Field(None, alias="channelId")
    link: Optional[str] = None


class Upgrade(BaseModel):
    """The upgrade object."""

    id: str
    name: str
    price: int
    profit_per_hour: int = Field(..., alias="profitPerHour")
    condition: Optional[Condition] = None
    section: str
    level: int
    current_profit_per_hour: int = Field(..., alias="currentProfitPerHour")
    profit_per_hour_delta: int = Field(..., alias="profitPerHourDelta")
    is_available: bool = Field(..., alias="isAvailable")
    is_expired: bool = Field(..., alias="isExpired")
    max_level: Optional[int] = Field(None, alias="maxLevel")
    expires_at: Optional[str] = Field(None, alias="expiresAt")
    cooldown_seconds: Optional[int] = Field(None, alias="cooldownSeconds")
    total_cooldown_seconds: Optional[int] = Field(None, alias="totalCooldownSeconds")
    welcome_coins: Optional[int] = Field(None, alias="welcomeCoins")

    @computed_field  # type: ignore
    @property
    def effective_pphd(self) -> Decimal:
        """Get the effective profit per hour delta."""
        if self.profit_per_hour_delta == 0:
            return Decimal(1_000_000_000)
        return Decimal(f"{self.price / self.profit_per_hour_delta:.2f}")


class Section(BaseModel):
    """The section object."""

    section: str
    is_available: bool = Field(..., alias="isAvailable")


class DailyCombo(BaseModel):
    """The daily combo object."""

    upgrade_ids: List[str] = Field(..., alias="upgradeIds")
    bonus_coins: int = Field(..., alias="bonusCoins")
    is_claimed: bool = Field(..., alias="isClaimed")
    remain_seconds: int = Field(..., alias="remainSeconds")


class UpgradesData(BaseModel):
    """The main model object."""

    upgrades_for_buy: List[Upgrade] = Field(..., alias="upgradesForBuy")
    sections: List[Section]
    daily_combo: DailyCombo = Field(..., alias="dailyCombo")

    model_config = ConfigDict(frozen=True)

    def get_most_profitable_upgrade(self, current_balance: int) -> Upgrade:
        """Get the most profitable upgrade."""
        ranked = sorted(
            (
                upg
                for upg in self.upgrades_for_buy
                if upg.is_available and not upg.is_expired and upg.profit_per_hour_delta > 0
            ),
            key=lambda x: x.effective_pphd,
        )

        median_rank = Decimal(numpy.median(numpy.array([upg.effective_pphd for upg in ranked])))

        available = sorted(
            [upg for upg in ranked if upg.cooldown_seconds is None and upg.effective_pphd <= median_rank],
            key=lambda x: (x.price // 100_000, x.effective_pphd),
        )

        for idx, upg in enumerate(available):
            if current_balance >= upg.price:
                return available[idx]

        return available[0]
