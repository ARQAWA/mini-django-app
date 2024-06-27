from django.db import models


class Info(models.Model):
    """Модель информации."""

    id = models.BigIntegerField(help_text="Telegram ID", primary_key=True)
    first_name = models.CharField(max_length=255, help_text="Telegram first name")
    last_name = models.CharField(max_length=255, help_text="Telegram last name", null=True)
    username = models.CharField(max_length=255, help_text="Telegram username", null=True)

    def __str__(self) -> str:
        return str(self.username or self.first_name or self.id)


class Account(models.Model):
    """Модель аккаунта."""

    init_data = models.CharField(max_length=4096, help_text="Account init data")
    proxy_url = models.CharField(max_length=2048, help_text="Account proxy URL")
    info = models.ForeignKey("games.Info", on_delete=models.RESTRICT, help_text="Account info")
    is_playing = models.BooleanField(help_text="Is account playing", default=False)

    def __str__(self) -> str:
        return str(self.info)


class Slot(models.Model):
    """Модель слота."""

    user_id = models.ForeignKey("users.Customer", on_delete=models.RESTRICT, help_text="User ID")
    hash_name = models.ForeignKey("core.Game", on_delete=models.RESTRICT, help_text="Game hash name")
    account = models.ForeignKey("games.Account", on_delete=models.RESTRICT, null=True, help_text="Account")
    expire_time = models.DateTimeField(help_text="Slot expire time")

    def __str__(self) -> str:
        return "Empty Slot" if not self.account else str(self.account)
