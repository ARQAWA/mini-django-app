from app.core.apps.stats.models import Play
from app.core.common.enums import ErrorsPhrases
from app.core.common.error import ApiError
from app.core.common.threaded_transaction import by_transaction


@by_transaction
def write_play_stats(
    account_id: int,
    balance: int,
    pph: int,
    pphd: int | None = None,
    taps: int | None = None,
    cards: int | None = None,
    tasks: int | None = None,
    combos: int | None = None,
    ciphers: int | None = None,
) -> None:
    """Записывает статистику игры в файл."""
    play: Play | None = Play.objects.select_for_update().filter(account_id=account_id).first()
    if play is None:
        raise ApiError.not_found(ErrorsPhrases.PLAY_STATS_NOT_FOUND)

    play.stats_dict["balance"] += balance
    play.stats_dict["pph"] += pph

    if pphd is not None:
        play.stats_dict["pphd"] += pphd

    if taps is not None:
        play.stats_dict["taps"] += taps

    if cards is not None:
        play.stats_dict["cards"] += cards

    if tasks is not None:
        play.stats_dict["tasks"] += tasks

    if combos is not None:
        play.stats_dict["combos"] += combos

    if ciphers is not None:
        play.stats_dict["ciphers"] += ciphers

    play.save()
