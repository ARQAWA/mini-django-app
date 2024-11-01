from dataclasses import dataclass, field
from typing import Any, Literal, TypedDict

from httpx import AsyncClient

from app.tap_robotics.hamster_kombat.dicts.clicker_tasks import ClickerTaskDict
from app.tap_robotics.hamster_kombat.dicts.clicker_upgrade import ClickerUpgradeDict
from app.tap_robotics.hamster_kombat.dicts.clicker_user import ClickerUserDict

task_action = Literal[
    "sync",
    "tap_hamster",
    "execute_tasks",
    "buy_upgrades",
    "finish",
]


class AccInfo(TypedDict):
    """Информация об аккаунте."""

    id: int
    auth_token: str
    user_agent: str
    proxy: str | None


@dataclass(frozen=True, slots=True)
class HamsterTask:
    """Задача для бота."""

    account_id: int
    auth_token: str
    user_agent: str

    action: task_action

    proxy_client: AsyncClient | None = field(default=None)

    user: ClickerUserDict | None = field(default=None)
    tasks: list[ClickerTaskDict] = field(default_factory=list)
    upgrades: list[ClickerUpgradeDict] = field(default_factory=list)

    stats_dict: dict[str, Any] = field(default_factory=dict)
    net_errors: dict[str, Any] = field(default_factory=dict)
    net_success: int = field(default=0)

    def next(
        self,
        action: task_action,
        *,
        user: ClickerUserDict | None = None,
        tasks: list[ClickerTaskDict] | None = None,
        upgrades: list[ClickerUpgradeDict] | None = None,
        stats_dict: dict[str, Any] | None = None,
        net_errors: dict[str, Any] | None = None,
        net_success: int | None = None,
    ) -> "HamsterTask":
        """Следующее действие."""
        stats_dict_ = self.stats_dict.copy()
        if stats_dict is not None:
            for key, value in stats_dict.items():
                if key not in stats_dict_:
                    stats_dict_[key] = 0
                stats_dict_[key] += value

        net_success_ = self.net_success
        if net_success is not None:
            net_success_ += net_success

        net_errors_ = self.net_errors.copy()
        if net_errors is not None:
            for key, value in net_errors.items():
                if key not in net_errors_:
                    net_errors_[key] = 0
                net_errors_[key] += value

        return HamsterTask(
            account_id=self.account_id,
            auth_token=self.auth_token,
            user_agent=self.user_agent,
            action=action,
            user=user or self.user,
            tasks=tasks or self.tasks,
            upgrades=upgrades or self.upgrades,
            stats_dict=stats_dict_,
            net_errors=net_errors_,
            net_success=net_success or self.net_success,
        )
