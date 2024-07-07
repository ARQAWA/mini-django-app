from functools import partial

from app.tap_robotics.hamster_kombat.dicts.clicker_upgrade import ClickerUpgradeDict


def get_most_profitable_upgrades(
    upgs: list[ClickerUpgradeDict],
    k: int,
) -> list[ClickerUpgradeDict]:
    """Получить список самых прибыльных апгрейдов."""
    conditions: dict[str, int] = {}
    for u in upgs:
        condition = u.get("condition")
        if condition is not None and condition["_type"] == "ByUpgrade":
            upg_id = condition["upgradeId"]
            conditions[upg_id] = max(conditions.get(upg_id, -1), condition["level"])

    upg_filter = partial(calculate_effective_pphd, conditions=conditions)

    return sorted(
        (
            upg
            for upg in upgs
            if upg["isAvailable"]
            and not upg["isExpired"]
            and upg["profitPerHourDelta"] > 0
            and not upg.get("cooldownSeconds")
        ),
        key=upg_filter,
    )[:k]


def calculate_effective_pphd(
    upg: ClickerUpgradeDict,
    conditions: dict[str, int],
) -> tuple[int, float]:
    """Рассчитать эффективный PPHD."""
    priority = 1
    if (target_level := conditions.get(upg["id"])) is not None and target_level > upg["level"]:
        priority = 0

    int(conditions.get(upg["id"], 0) < upg["level"])

    if upg["profitPerHourDelta"] == 0:
        return 2, 1_000_000_000
    return priority, upg["price"] / upg["profitPerHourDelta"]
