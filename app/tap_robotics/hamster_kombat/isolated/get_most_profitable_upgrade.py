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

    sorted_upgs = sorted(
        (
            upg
            for upg in upgs
            if upg["isAvailable"]
            and not upg["isExpired"]
            and upg["profitPerHourDelta"] > 0
            and not upg.get("cooldownSeconds")
        ),
        key=calculate_effective_pphd,
    )

    result = sorted_upgs[:k]

    uniq_upg_ids = set(upg["id"] for upg in result)
    result += [
        upg for upg in sorted_upgs if upg["id"] not in uniq_upg_ids and conditions.get(upg["id"], 0) > upg["level"]
    ]

    return result


def calculate_effective_pphd(
    upg: ClickerUpgradeDict,
) -> float:
    """Рассчитать эффективный PPHD."""
    if upg["profitPerHourDelta"] == 0:
        return 1_000_000_000
    return upg["price"] / upg["profitPerHourDelta"]
