"""Config module for the application settings."""

from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Config class for the application settings."""

    model_config = SettingsConfigDict(
        env_file="src\\backend\\.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    mongo_url: Optional[str] = None
    mongo_db: Optional[str] = None


settings: Settings = Settings()
