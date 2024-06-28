from django.db import models


class Play(models.Model):
    """Модель игровой статистики."""

    account = models.OneToOneField("games.Account", on_delete=models.CASCADE, help_text="Account", related_name="play")

    balance = models.BigIntegerField(default=0, help_text="Balance")
    pph = models.BigIntegerField(default=0, help_text="PPH")

    pphd = models.BigIntegerField(default=0, help_text="Stat PPHD")
    taps = models.BigIntegerField(default=0, help_text="Stat Taps")
    cards = models.BigIntegerField(default=0, help_text="Stat Bought Cards")
    tasks = models.BigIntegerField(default=0, help_text="Stat Tasks")
    combos = models.BigIntegerField(default=0, help_text="Stat Combos")
    ciphers = models.BigIntegerField(default=0, help_text="Stat Ciphers")

    def __str__(self) -> str:
        return f"{self.account} / Balance: {self.balance / 1_000_000:.2f}M"

    def reset(self) -> None:
        """Сброс статистики."""
        self.pphd = 0
        self.taps = 0
        self.cards = 0
        self.tasks = 0
        self.combos = 0
        self.ciphers = 0
        self.save()


class Network(models.Model):
    """Модель сетевой статистики."""

    account = models.OneToOneField(
        "games.Account", on_delete=models.CASCADE, help_text="Account", related_name="network"
    )

    success_percent = models.DecimalField(default=0, max_digits=5, decimal_places=2, help_text="Stat Success Percent")
    success = models.BigIntegerField(default=0, help_text="Stat Success")
    errors = models.BigIntegerField(default=0, help_text="Stat Errors")
    errors_codes = models.JSONField(default=dict, help_text="Stat Error Codes")

    def __str__(self) -> str:
        return f"{self.account.customer} : {self.success_percent:.2f}% ({self.success} / {self.errors})"

    def calculate_success_percent(self, save: bool = True) -> None:
        """Расчет процента успешных запросов."""
        self.success_percent = self.success / ((self.success + self.errors) or 1) * 100
        if save:
            self.save()

    def reset(self) -> None:
        """Сброс статистики."""
        self.success = 0
        self.errors = 0
        self.errors_codes = {}
        self.calculate_success_percent(False)
        self.save()
