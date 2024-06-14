from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class SentrySettings(BaseModel):
    """Настройки Sentry."""

    dsn: str


class PostgresSettings(BaseModel):
    """Настройки Postgres."""

    host: str
    port: int
    user: str
    password: str
    database: str
    pool_min_size: int = 1
    pool_max_size: int = 20


class TelegramSettings(BaseModel):
    """Настройки Telegram."""

    token: str


class Settings(BaseSettings):
    """Настройки приложения."""

    sentry: SentrySettings
    postgres: PostgresSettings
    telegram_bot: TelegramSettings
    web_app_url: str

    model_config = SettingsConfigDict(
        frozen=True,
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )


envs = Settings()  # type: ignore
