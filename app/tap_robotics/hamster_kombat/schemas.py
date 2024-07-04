from dataclasses import dataclass
from typing import Literal, TypedDict

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
    next_action: task_action

    def next(self, action: task_action) -> "HamsterTask":
        """Следующее действие."""
        return HamsterTask(
            account_id=self.account_id,
            auth_token=self.auth_token,
            user_agent=self.user_agent,
            action=self.next_action,
            next_action=action,
        )
