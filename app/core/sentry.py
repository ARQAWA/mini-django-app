import os

from django.core.handlers.asgi import ASGIHandler

Handler = ASGIHandler


def get_sentry_wraped_app(app: ASGIHandler) -> ASGIHandler:
    """Инициализация Sentry."""
    if (sentry_dsn := os.environ.get("SENTRY__DSN", None)) is not None:
        import sentry_sdk  # noqa
        from sentry_sdk.integrations.asgi import SentryAsgiMiddleware  # noqa

        sentry_sdk.init(dsn=sentry_dsn)
        print("Sentry is running")  # noqa

        return SentryAsgiMiddleware(app)  # type: ignore

    return app
