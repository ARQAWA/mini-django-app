from django.core.asgi import get_asgi_application

from app.core.common.sentry import get_sentry_wraped_app

application = get_sentry_wraped_app(app=get_asgi_application())
