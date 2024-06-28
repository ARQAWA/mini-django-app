from typing import Literal

from django.db import models

from app.core.common.enums import ModelEnum


class Game(models.Model):
    """Модель игры."""

    id = models.CharField(primary_key=True, help_text="Game ID")
    name = models.CharField(help_text="Game name")
    is_active = models.BooleanField(help_text="Is game active")

    def __str__(self) -> str:
        return self.name

    GAMES_LITERAL = Literal["hamster-kombat",]

    GAMES_DICT = {
        "hamster-kombat": "Hamster Kombat",
    }


class Payment(models.Model):
    """Модель платежа."""

    class Type(ModelEnum):
        """Тип платежа."""

        TON = "TON"
        DEMO = "DEMO"

    id = models.TextField(primary_key=True, help_text="Payment ID")
    type = models.CharField(choices=Type.choices(), help_text="Payment type")
    amount = models.DecimalField(max_digits=16, decimal_places=6, help_text="Payment amount")
    is_payed = models.BooleanField(db_index=True, help_text="Is payment payed")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, help_text="Payment created at")

    def __str__(self) -> str:
        return f"{self.id} / {self.amount} / {self.is_payed} / {self.slot}"


class Customer(models.Model):
    """Модель покупателя."""

    id = models.BigIntegerField(primary_key=True, help_text="User ID")
    first_name = models.CharField(help_text="First name")
    last_name = models.CharField(null=True, help_text="Last name")
    username = models.CharField(null=True, help_text="Username")
    refresh_token = models.CharField(db_index=True, help_text="Refresh token")

    def __str__(self) -> str:
        return str(self.username or self.first_name or self.id)
