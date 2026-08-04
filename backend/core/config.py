"""
Application configuration loaded from environment variables and .env file.

Uses Pydantic Settings for validation and type-safe access.
"""

from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration for the SentinelAI backend."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = Field(default="SentinelAI", description="Application display name")
    app_env: str = Field(default="development", description="Runtime environment")
    debug: bool = Field(default=False, description="Enable debug mode")

    # Server
    host: str = Field(default="0.0.0.0", description="Server bind host")
    port: int = Field(default=8000, description="Server bind port")

    # CORS
    cors_origins: str = Field(
        default="http://localhost:3000,http://localhost:8501",
        description="Comma-separated allowed CORS origins",
    )

    # Database
    database_url: str = Field(
        default="sqlite:///./sentinelai.db",
        description="SQLAlchemy database connection URL",
    )

    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    log_dir: str = Field(default="logs", description="Directory for log files")

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse comma-separated CORS origins into a list."""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance (singleton)."""
    return Settings()
