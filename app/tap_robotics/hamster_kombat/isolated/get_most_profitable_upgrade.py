from app.tap_robotics.hamster_kombat.dicts.clicker_upgrade import ClickerUpgradeDict


def get_most_profitable_upgrades(
    upgs: list[ClickerUpgradeDict],
    k: int,
    max_level: int,
) -> list[ClickerUpgradeDict]:
    """Получить список самых прибыльных апгрейдов."""
    ranked_sorted = sorted(
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

    return [upg for idx, upg in enumerate(ranked_sorted) if idx < k or upg["level"] < max_level]


def calculate_effective_pphd(upg: ClickerUpgradeDict) -> float:
    """Рассчитать эффективный PPHD."""
    if upg["profitPerHourDelta"] == 0:
        return 1_000_000_000
    return upg["price"] / upg["profitPerHourDelta"]
