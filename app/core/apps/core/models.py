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
