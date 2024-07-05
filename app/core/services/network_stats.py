from app.core.apps.stats.models import Network
from app.core.common.enums import ErrorsPhrases
from app.core.common.error import ApiError
from app.core.common.threaded_transaction import by_transaction


@by_transaction
def write_network_stats(
    account_id: int,
    success: int,
    errors_codes: dict[str, int],
) -> None:
    """Записывает статистику сети."""
    network: Network | None = Network.objects.select_for_update().filter(account_id=account_id).first()
    if network is None:
        raise ApiError.not_found(ErrorsPhrases.NETWORK_STATS_NOT_FOUND)

    network.success += success
    network.errors += sum(errors_codes.values())
    for code, count in errors_codes.items():
        if code not in network.errors_codes:
            network.errors_codes[code] = 0
        network.errors_codes[code] += count
    network.calculate_success_percent()
