from django.db import models

from app.core.models.user_data import UserData


class Customer(models.Model):
    """Модель покупателя."""

    username = models.CharField(max_length=150, unique=True, db_index=True, help_text="Username")
    first_name = models.CharField(max_length=150, help_text="First name")
    last_name = models.CharField(max_length=150, null=True, blank=True, help_text="Last name")
    is_active = models.BooleanField(default=True, db_index=True, help_text="Is user active")
    refresh_token = models.CharField(max_length=256, db_index=True, help_text="Refresh token")

    def __str__(self) -> str:
        return self.username

    @property
    def user_obj(self) -> UserData.Dict:
        """Получение объекта пользователя."""
        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }
