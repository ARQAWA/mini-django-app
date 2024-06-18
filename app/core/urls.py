from django.urls import path

from app.api import init_api

api = init_api()

urlpatterns = [
    # path("admin/", admin.site.urls),
    path("api/", api.urls),
]
