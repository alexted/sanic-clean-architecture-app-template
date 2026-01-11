import os
from enum import StrEnum
from functools import lru_cache

from dotenv import load_dotenv
import msgspec

load_dotenv()


class EnvironmentEnum(StrEnum):
    LOCAL = "LOCAL"
    TESTING = "TESTING"
    TEST = "TEST"
    DEV = "DEV"
    STAGE = "STAGE"
    PROD = "PROD"


class LoggingLevelEnum(StrEnum):
    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"


class AppConfig(msgspec.Struct, frozen=True, kw_only=True):
    ENVIRONMENT: EnvironmentEnum = EnvironmentEnum.LOCAL
    APP_NAME: str = "xyu"

    # Logging
    SENTRY_DSN: str | None = None
    LOG_LEVEL: LoggingLevelEnum = LoggingLevelEnum.INFO
    TELEMETRY_URL: str | None = None

    # Postgres
    POSTGRES_DSN: str
    POSTGRES_MAX_CONNECTIONS: int = 10

    # Redis
    CACHE_DSN: str

    # Kafka
    KAFKA_DSN: str

    # Identity provider
    IDP_URL: str
    IDP_CLIENT_SECRET: str


@lru_cache(maxsize=1)
def get_config() -> AppConfig:
    # Собираем словарь из переменных окружения, которые есть в AppConfig
    # Это простой и быстрый способ без тяжелых зависимостей
    config_data = {}
    for field in msgspec.structs.fields(AppConfig):
        env_value = os.getenv(field.name)
        if env_value is not None:
            config_data[field.name] = env_value
        elif field.default is msgspec.NODEFAULT:
            # Если значения нет в env и нет дефолта в структуре - возникнет ошибка позже
            pass

    # msgspec.convert сделает всю магию: приведет строки к int, Enum и т.д.
    return msgspec.convert(config_data, AppConfig)
