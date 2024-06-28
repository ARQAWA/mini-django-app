from django.db import models


class Play(models.Model):
    """Модель игровой статистики."""

    account = models.OneToOneField("games.Account", on_delete=models.CASCADE, help_text="Account")

    balance = models.DecimalField(default=0, max_digits=16, decimal_places=6, help_text="Stat Balance")
    pph = models.DecimalField(default=0, max_digits=16, decimal_places=6, help_text="Stat PPH")

    taps = models.BigIntegerField(default=0, help_text="Stat Taps")
    cards = models.BigIntegerField(default=0, help_text="Stat Bought Cards")
    tasks = models.BigIntegerField(default=0, help_text="Stat Tasks")
    combos = models.BigIntegerField(default=0, help_text="Stat Combos")
    ciphers = models.BigIntegerField(default=0, help_text="Stat Ciphers")

    def __str__(self) -> str:
        return f"{self.account} / Balance: {self.balance / 1_000_000:.2f}M"


class Network(models.Model):
    """Модель сетевой статистики."""

    account = models.OneToOneField("games.Account", on_delete=models.CASCADE, help_text="Account")

    success_percent = models.DecimalField(default=100, max_digits=5, decimal_places=2, help_text="Stat Success Percent")
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
