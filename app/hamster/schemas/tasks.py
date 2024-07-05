from typing import TypedDict

# class LinkWithLocale(TypedDict):
#     """The link with locale object."""
#     locale: str
#     link: str


# class RewardByDay(TypedDict):
#     """The reward by day object."""
#     days: int
#     rewardCoins: int


class Task(TypedDict):
    """The task object."""

    id: str
    # rewardCoins: int
    # periodicity: str
    # link: str | None
    # linksWithLocales: list[LinkWithLocale] | None
    isCompleted: bool
    # completedAt: str | None
    # channelId: int | None
    # rewardsByDays: list[dict] | None
    # days: int | None
    # remainSeconds: int | None
