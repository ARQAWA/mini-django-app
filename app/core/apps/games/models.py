from django.db import models

from app.core.common.db_date import utc_now_plus_month


class Info(models.Model):
    """Модель информации."""

    id = models.BigIntegerField(primary_key=True, help_text="User ID")
    first_name = models.CharField(max_length=255, help_text="First name")
    last_name = models.CharField(max_length=255, help_text="Last name", null=True)
    username = models.CharField(max_length=255, help_text="Username", null=True)

    def __str__(self) -> str:
        return str(self.username or self.first_name or self.id)


class Account(models.Model):
    """Модель аккаунта."""

    init_data = models.CharField(max_length=4096, help_text="Init data")
    proxy_url = models.CharField(max_length=2048, help_text="Proxy URL")
    auth_token = models.CharField(max_length=2048, help_text="Auth token", null=True)
    info = models.OneToOneField("games.Info", on_delete=models.RESTRICT, help_text="Info")
    is_playing = models.BooleanField(help_text="Is account playing", default=False)

    def __str__(self) -> str:
        return str(self.info)


class Slot(models.Model):
    """Модель слота."""

    user = models.OneToOneField("users.Customer", on_delete=models.RESTRICT, help_text="User")
    game = models.OneToOneField("core.Game", on_delete=models.RESTRICT, help_text="Game")
    account = models.OneToOneField("games.Account", null=True, on_delete=models.RESTRICT, help_text="Account")
    expired_at = models.DateTimeField(default=utc_now_plus_month, db_index=True, help_text="Slot expired at")

    def __str__(self) -> str:
        return "Empty Slot" if not self.account else str(self.account)
