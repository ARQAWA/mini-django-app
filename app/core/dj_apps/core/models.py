from django.db import models


class Game(models.Model):
    """Модель игры."""

    hash_name = models.CharField(max_length=255, primary_key=True, help_text="Game hash name")
    name = models.CharField(max_length=255, help_text="Game name")
    is_active = models.BooleanField(help_text="Is game active")

    def __str__(self) -> str:
        return self.name
