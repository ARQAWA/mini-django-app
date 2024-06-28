from django.db import models


class Customer(models.Model):
    """Модель покупателя."""

    first_name = models.CharField(max_length=150, help_text="First name")
    last_name = models.CharField(max_length=150, null=True, help_text="Last name")
    username = models.CharField(max_length=150, null=True, help_text="Username")
    refresh_token = models.CharField(max_length=256, db_index=True, help_text="Refresh token")

    def __str__(self) -> str:
        return str(self.username or self.first_name or self.id)
