from django.db import models

from app.core.common.db_date import utc_now_plus_month


class Account(models.Model):
    """Модель аккаунта."""

    tg_id = models.BigIntegerField(help_text="Telegram ID")
    first_name = models.CharField(max_length=255, help_text="First name")
    last_name = models.CharField(max_length=255, null=True, help_text="Last name")
    username = models.CharField(max_length=255, null=True, help_text="Username")

    init_data = models.CharField(max_length=4096, help_text="Init data")
    proxy_url = models.CharField(max_length=2048, null=True, help_text="Proxy URL")

    is_playing = models.BooleanField(default=False, help_text="Is account playing")

    auth_token = models.CharField(max_length=2048, null=True, help_text="Auth token")

    game = models.ForeignKey("core.Game", on_delete=models.RESTRICT, help_text="Game")
    customer = models.ForeignKey("core.Customer", on_delete=models.RESTRICT, help_text="User")

    class Meta:
        """Метаинформация модели."""

        unique_together = (("tg_id", "customer", "game"),)

    def __str__(self) -> str:
        return f"{self.customer} / " f"{self.game} / " f"{self.username or self.first_name or self.id}"


class Slot(models.Model):
    """Модель слота."""

    game = models.ForeignKey("core.Game", on_delete=models.RESTRICT, help_text="Game")
    customer = models.ForeignKey("core.Customer", on_delete=models.RESTRICT, help_text="User")

    account = models.OneToOneField(
        "games.Account", null=True, on_delete=models.SET_NULL, help_text="Account", related_name="slot"
    )

    payment = models.OneToOneField("core.Payment", on_delete=models.RESTRICT, help_text="Payment", related_name="slot")
    expired_at = models.DateTimeField(default=utc_now_plus_month, db_index=True, help_text="Slot expired at")

    def __str__(self) -> str:
        return "Empty Slot" if not self.account else str(self.account)
