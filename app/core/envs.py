from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthSettings(BaseModel):
    """Настройки авторизации."""

    auth_token_ttl: int = 60 * 5
    access_token_ttl: int = 60 * 60 * 8
    refresh_token_ttl: int = 60 * 60 * 24 * 14


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


class HamsterSettings(BaseModel):
    """Настройки Hamster."""

    token: str
    user_agent: str


class RedisSettings(BaseModel):
    """Настройки Redis."""

    host: str
    port: int
    db: int

    @property
    def dsn(self) -> str:
        """Возвращает DSN."""
        return f"redis://{self.host}:{self.port}/{self.db}"


class TonClientSettings(BaseModel):
    """Настройки TonClient."""

    base_url: str
    payment_address: str


class Settings(BaseSettings):
    """Настройки приложения."""

    is_local: bool = False
    django_secret_key: str
    django_settings_module: str
    allowed_hosts: str
    bros_secret_token: str
    auth: AuthSettings = Field(default_factory=AuthSettings)
    sentry: SentrySettings | None = None
    postgres: PostgresSettings
    redis: RedisSettings
    ton_client: TonClientSettings
    telegram_bot: TelegramSettings
    hamster: HamsterSettings | None = None

    model_config = SettingsConfigDict(
        frozen=True,
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )


envs = Settings()  # type: ignore
