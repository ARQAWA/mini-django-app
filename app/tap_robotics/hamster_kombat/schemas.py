from dataclasses import dataclass, field
from typing import Literal, TypedDict

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

    def next(
        self,
        action: task_action,
        *,
        user: ClickerUserDict | None = None,
        tasks: list[ClickerTaskDict] | None = None,
        upgrades: list[ClickerUpgradeDict] | None = None,
    ) -> "HamsterTask":
        """Следующее действие."""
        return HamsterTask(
            account_id=self.account_id,
            auth_token=self.auth_token,
            user_agent=self.user_agent,
            action=action,
            user=user or self.user,
            tasks=tasks or self.tasks,
            upgrades=upgrades or self.upgrades,
        )
