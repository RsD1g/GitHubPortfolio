# backend/app/config.py
"""Settings configuration using pydantic-settings."""
from pydantic import BaseSettings, Field
from typing import Optional

class Settings(BaseSettings):
    # Core settings
    GITHUB_TOKEN: Optional[str] = Field(None, description="GitHub personal access token")
    GITHUB_USERNAME: Optional[str] = Field(None, description="GitHub username for sync")
    ADMIN_TOKEN: str = Field(..., description="Admin authentication token for /sync endpoint")
    DATABASE_URL: str = Field(..., description="PostgreSQL connection URL")
    REDIS_URL: str = Field(..., description="Redis connection URL")
    CORS_ORIGINS: str = Field(..., description="Comma-separated list of allowed origins")
    SYNC_HOUR_UTC: int = Field(4, description="Hour in UTC for daily sync")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()