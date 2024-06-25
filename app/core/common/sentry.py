from django.core.handlers.asgi import ASGIHandler
from loguru import logger

from app.core.envs import envs

Handler = ASGIHandler


def sentry_init() -> bool:
    """Инициализация Sentry."""
    if not envs.sentry:
        return False

    import sentry_sdk  # noqa

    sentry_sdk.init(dsn=envs.sentry.dsn)
    logger.debug("Sentry is running")  # noqa
    return True


def get_sentry_wraped_app(app: ASGIHandler) -> ASGIHandler:
    """Инициализация Sentry для ASGI-приложения."""
    if sentry_init():
        from sentry_sdk.integrations.asgi import SentryAsgiMiddleware  # noqa

        return SentryAsgiMiddleware(app)  # type: ignore

    return app
