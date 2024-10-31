import time

from app.tap_robotics.hamster_kombat.dicts.clicker_user import ClickerUserDict


def get_available_taps(user: ClickerUserDict) -> tuple[int, int]:
    """
    Получить тапы и доступные тапы.

    :param user: Данные пользователя.
    :return: Количество тапов и доступных тапов.
    """
    available_taps = user["availableTaps"]
    extra_taps = int((time.time() - user["lastSyncUpdate"]) * user["tapsRecoverPerSec"])

    if extra_taps > 0:
        available_taps += extra_taps

    if available_taps > user["maxTaps"]:
        available_taps = user["maxTaps"]

    count = available_taps // user["earnPerTap"]

    return count, available_taps
