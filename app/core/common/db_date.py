from datetime import UTC, datetime

from dateutil.relativedelta import relativedelta


def utc_now_plus_month() -> datetime:
    """Возвращает текущую дату и время плюс месяц."""
    return datetime.now(UTC) + relativedelta(months=1)


def demo_expired() -> datetime:
    """Возвращает текущую дату и время плюс 3 часа 30 минут."""
    # return datetime.now(UTC) + relativedelta(hours=3, minutes=30)
    return datetime.now(UTC) + relativedelta(days=14, minutes=30)


def utc_now() -> datetime:
    """Возвращает текущую дату и время."""
    return datetime.now(UTC)
