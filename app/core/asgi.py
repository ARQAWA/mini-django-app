import os

from django.core.asgi import get_asgi_application

from app.core.sentry import sentry_init

sentry_ready = sentry_init()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.core.settings")
application = get_asgi_application()

if sentry_ready:
    from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

    application = SentryAsgiMiddleware(application)  # type: ignore
