"""Application configuration.

Settings are loaded from environment variables and an optional ``.env``
file via Pydantic v2. Never commit real secrets — see ``.env.example``.
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    project_name: str = "Intelligent Business Automation & Management System"
    version: str = "0.1.0"
    debug: bool = Field(default=False)

    api_v1_prefix: str = "/api/v1"
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]

    # Security
    secret_key: str = "change-me-in-production"
    access_token_expire_minutes: int = 30
    algorithm: str = "HS256"

    # Data stores (used by later modules)
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/ibam"
    redis_url: str = "redis://localhost:6379/0"


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance (read once at startup)."""
    return Settings()
