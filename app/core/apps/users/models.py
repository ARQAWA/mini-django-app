from django.db import models

from app.core.models.user_data import UserData


class Customer(models.Model):
    """Модель покупателя."""

    first_name = models.CharField(max_length=150, help_text="First name")
    last_name = models.CharField(max_length=150, null=True, help_text="Last name")
    username = models.CharField(max_length=150, null=True, help_text="Username")
    has_trial = models.BooleanField(default=True, help_text="Has trial")
    is_active = models.BooleanField(default=True, db_index=True, help_text="Is user active")
    refresh_token = models.CharField(max_length=256, db_index=True, help_text="Refresh token")

    def __str__(self) -> str:
        return str(self.username or self.first_name or self.id)

    @property
    def user_obj(self) -> UserData.Dict:
        """Получение объекта пользователя."""
        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }
