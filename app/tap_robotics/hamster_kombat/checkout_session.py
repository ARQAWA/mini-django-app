from datetime import timedelta

from django.db.models.functions import Now

from app.core.apps.games.models import Session
from app.core.common.threaded_transaction import by_transaction


@by_transaction
def write_checkpoint(account_id: int, errors: bool = False) -> None:
    """Записать чекпоинт для сессии."""
    delta = timedelta(minutes=15) if errors else timedelta(minutes=3)
    Session.objects.filter(account_id=account_id).update(next_at=Now() + delta, errors=0)
