import os

from django.core.asgi import get_asgi_application

from app.core.sentry import get_sentry_wraped_app

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.core.settings")

application = get_sentry_wraped_app(app=get_asgi_application())
