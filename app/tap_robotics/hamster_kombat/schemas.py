from dataclasses import dataclass, field
from typing import Any, Literal, TypedDict

from app.tap_robotics.hamster_kombat.dicts.clicker_tasks import ClickerTaskDict
from app.tap_robotics.hamster_kombat.dicts.clicker_upgrade import ClickerUpgradeDict
from app.tap_robotics.hamster_kombat.dicts.clicker_user import ClickerUserDict

task_action = Literal[
    "sync",
    "tap_hamster",
    "execute_tasks",
    "buy_upgrades",
]


class AccInfo(TypedDict):
    """Информация об аккаунте."""

    id: int
    auth_token: str
    user_agent: str


@dataclass(frozen=True, slots=True)
class HamsterTask:
    """Задача для бота."""

    account_id: int
    auth_token: str
    user_agent: str

    action: task_action

    user: ClickerUserDict | None = field(default=None)
    tasks: list[ClickerTaskDict] = field(default_factory=list)
    upgrades: list[ClickerUpgradeDict] = field(default_factory=list)

    stats_dict: dict[str, Any] = field(default_factory=dict)
    net_dict: dict[str, Any] = field(default_factory=dict)

    def next(
        self,
        action: task_action,
        *,
        user: ClickerUserDict | None = None,
        tasks: list[ClickerTaskDict] | None = None,
        upgrades: list[ClickerUpgradeDict] | None = None,
        stats_dict: dict[str, Any] | None = None,
        net_dict: dict[str, Any] | None = None,
    ) -> "HamsterTask":
        """Следующее действие."""
        stats_dict_ = self.stats_dict.copy()
        if stats_dict is not None:
            for key, value in stats_dict.items():
                if key not in stats_dict_:
                    stats_dict_[key] = 0
                stats_dict_[key] += value

        net_dict_ = self.net_dict.copy()
        if net_dict is not None:
            for key, value in net_dict.items():
                if key not in net_dict_:
                    net_dict_[key] = 0
                net_dict_[key] += value

        return HamsterTask(
            account_id=self.account_id,
            auth_token=self.auth_token,
            user_agent=self.user_agent,
            action=action,
            user=user or self.user,
            tasks=tasks or self.tasks,
            upgrades=upgrades or self.upgrades,
            stats_dict=stats_dict_,
            net_dict=net_dict_,
        )
