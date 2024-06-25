import time
from datetime import datetime
from typing import Any, Dict, List, Optional

from loguru import logger
from pydantic import BaseModel, ConfigDict, Field


class Boost(BaseModel):
    """The boost object."""

    id: str
    level: int
    last_upgrade_at: int = Field(alias="lastUpgradeAt")


class Upgrade(BaseModel):
    """The upgrade object."""

    id: str
    level: int
    last_upgrade_at: int = Field(alias="lastUpgradeAt")
    snapshot_referrals_count: Optional[int] = Field(alias="snapshotReferralsCount", default=0)


class Task(BaseModel):
    """The task object."""

    id: str
    completed_at: Optional[datetime] = Field(alias="completedAt", default=None)


class ReferralFriend(BaseModel):
    """The referral friend object."""

    is_bot: bool = Field(alias="isBot")
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    added_to_attachment_menu: Optional[bool] = Field(alias="addedToAttachmentMenu", default=None)
    id: int
    is_premium: Optional[bool] = Field(alias="isPremium", default=None)
    can_read_all_group_messages: Optional[bool] = Field(alias="canReadAllGroupMessages", default=None)
    language_code: str = Field(alias="languageCode")
    can_join_groups: Optional[bool] = Field(alias="canJoinGroups", default=None)
    supports_inline_queries: Optional[bool] = Field(alias="supportsInlineQueries", default=None)
    photos: List[str] = Field(default=[])
    username: str
    welcome_bonus_coins: int = Field(alias="welcomeBonusCoins")


class Referral(BaseModel):
    """The referral object."""

    friend: ReferralFriend


class ClickerUser(BaseModel):
    """The main user object."""

    id: str
    total_coins: float = Field(alias="totalCoins")
    balance_coins: float = Field(alias="balanceCoins")
    level: int
    available_taps: int = Field(alias="availableTaps")
    last_sync_update: int = Field(alias="lastSyncUpdate")
    exchange_id: str = Field(alias="exchangeId")
    boosts: Dict[str, Boost]
    upgrades: Dict[str, Upgrade]
    tasks: Dict[str, Task]
    airdrop_tasks: Dict[str, Task] = Field(alias="airdropTasks")
    referrals_count: int = Field(alias="referralsCount")
    max_taps: int = Field(alias="maxTaps")
    earn_per_tap: int = Field(alias="earnPerTap")
    earn_passive_per_sec: float = Field(alias="earnPassivePerSec")
    earn_passive_per_hour: int = Field(alias="earnPassivePerHour")
    last_passive_earn: float = Field(alias="lastPassiveEarn")
    taps_recover_per_sec: int = Field(alias="tapsRecoverPerSec")
    referral: Referral
    balance_tickets: int | None = Field(None, alias="balanceTickets")
    claimed_upgrade_combo_at: Optional[datetime] = Field(alias="claimedUpgradeComboAt", default=None)
    sync_time: float = Field(default_factory=time.time)

    model_config = ConfigDict(frozen=True)

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        logger.debug(
            f"Balance: {self.balance_coins:,.0f}; "
            f"Energy: {self.available_taps:,}/{self.max_taps:,}; "
            f"Multiplier: {self.earn_per_tap:,};"
        )
