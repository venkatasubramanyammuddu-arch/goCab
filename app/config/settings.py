from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Field names map to environment variables, case-insensitive:
    # database_url <- DATABASE_URL, redis_url <- REDIS_URL.
    # No defaults, so the app refuses to start if one is missing.
    database_url: str
    redis_url: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    # Built once, then reused: the environment is read a single time.
    return Settings()
