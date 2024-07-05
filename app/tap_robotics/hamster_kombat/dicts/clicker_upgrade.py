from typing import TypedDict


class ClickerUpgradeDict(TypedDict):
    """Clicker upgrade dict."""

    id: str
    price: int
    profitPerHourDelta: int
    isExpired: bool
    isAvailable: bool
    cooldownSeconds: int | None



class ClickerDailyComboDict(TypedDict):
    """Clicker daily combo dict."""

    upgradeIds: list[str]
    isClaimed: bool


#     @computed_field  # type: ignore
#     @property
#     def effective_pphd(self) -> Decimal:
#         """Get the effective profit per hour delta."""
#         if self.profit_per_hour_delta == 0:
#             return Decimal(1_000_000_000)
#         return Decimal(f"{self.price / self.profit_per_hour_delta:.2f}")
#
#
#     @property
#     def can_claim_combo(self) -> bool:
#         """Check if the combo can be claimed."""
#         return not self.daily_combo.is_claimed and len(self.daily_combo.upgrade_ids) == 3
#
#
#     def get_most_profitable_upgrades(self) -> list[Upgrade]:
#         """Get the most profitable upgrade."""
#         return sorted(
#             (
#                 upg
#                 for upg in self.upgrades_for_buy
#                 if upg.is_available
#                 and not upg.is_expired
#                 and upg.profit_per_hour_delta > 0
#                 and not upg.cooldown_seconds
#             ),
#             key=lambda x: x.effective_pphd,
#         )
