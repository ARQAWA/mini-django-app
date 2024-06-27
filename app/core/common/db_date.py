from datetime import UTC, datetime

from dateutil.relativedelta import relativedelta


def utc_now_plus_month() -> datetime:
    """Возвращает текущую дату и время плюс месяц."""
    return datetime.now(UTC) + relativedelta(months=1)
