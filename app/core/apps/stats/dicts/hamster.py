from typing import TypedDict


class HamsterStatsSchema:
    """Схема для статистики игры Hamster."""

    class Dict(TypedDict):
        """Словарь для статистики игры Hamster."""

        balance: int
        pph: int

        pphd: int
        taps: int
        cards: int
        tasks: int
        combos: int
        ciphers: int

    @classmethod
    def get_hamster_dict(cls) -> "HamsterStatsSchema.Dict":
        """Возвращает пустой словарь."""
        return {
            "balance": 0,
            "pph": 0,
            "pphd": 0,
            "taps": 0,
            "cards": 0,
            "tasks": 0,
            "combos": 0,
            "ciphers": 0,
        }
