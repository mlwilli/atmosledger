from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    env: str = "dev"
    log_level: str = "INFO"

    database_url: str
    redis_url: str
    rq_queue: str = "default"

    open_meteo_base_url: str = "https://api.open-meteo.com/v1"
    open_meteo_archive_base_url: str = "https://archive-api.open-meteo.com/v1"


settings = Settings()
