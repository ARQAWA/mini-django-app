from django.db import models

from app.core.models.user_data import UserData


class Customer(models.Model):
    """Модель покупателя."""

    username = models.CharField(max_length=150, unique=True, db_index=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    is_active = models.BooleanField(default=True, db_index=True)
    refresh_token = models.CharField(max_length=256, db_index=True)

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
