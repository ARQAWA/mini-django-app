from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Настойки приложения пользователей."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "app.users"
