from django.core.asgi import get_asgi_application

from app.core.common.ninjas_fix.shutdown_event import setup_shutdown_event
from app.core.common.sentry import get_sentry_wraped_app

setup_shutdown_event()
app = get_sentry_wraped_app(app=get_asgi_application())
