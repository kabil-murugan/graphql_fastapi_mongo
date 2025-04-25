"""Config module for the application settings."""

from typing import Optional

from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(find_dotenv())


class Settings(BaseSettings):
    """Config class for the application settings."""

    mongo_url: Optional[str] = None
    mongo_db: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None


settings: Settings = Settings()
