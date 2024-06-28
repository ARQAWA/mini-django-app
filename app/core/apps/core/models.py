from typing import Literal

from django.db import models


class Game(models.Model):
    """Модель игры."""

    id = models.CharField(max_length=255, primary_key=True, help_text="Game ID")
    name = models.CharField(max_length=255, help_text="Game name")
    is_active = models.BooleanField(help_text="Is game active")

    def __str__(self) -> str:
        return self.name

    GAMES_LITERAL = Literal["hamster-kombat",]

    GAMES_DICT = {
        "hamster-kombat": "Hamster Kombat",
    }


class Payment(models.Model):
    """Модель платежа."""

    id = models.CharField(max_length=64, primary_key=True, help_text="Payment ID")
    amount = models.DecimalField(max_digits=16, decimal_places=6, help_text="Payment amount")
    is_payed = models.BooleanField(help_text="Is payment payed")

    def __str__(self) -> str:
        return f"{self.id} / {self.amount} / {self.is_payed} / {self.slot}"


class Customer(models.Model):
    """Модель покупателя."""

    id = models.BigIntegerField(primary_key=True, help_text="User ID")
    first_name = models.CharField(max_length=150, help_text="First name")
    last_name = models.CharField(max_length=150, null=True, help_text="Last name")
    username = models.CharField(max_length=150, null=True, help_text="Username")
    refresh_token = models.CharField(max_length=256, db_index=True, help_text="Refresh token")

    def __str__(self) -> str:
        return str(self.username or self.first_name or self.id)
