import os


def sentry_init() -> bool:
    """Инициализация Sentry."""
    if (sentry_dsn := os.environ.get("SENTRY__DSN", None)) is not None:
        import sentry_sdk  # noqa

        sentry_sdk.init(dsn=sentry_dsn)
        print("Sentry is running")  # noqa

        return True
    return False
