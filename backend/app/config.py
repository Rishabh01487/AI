"""Pydantic settings for application configuration."""
from pydantic import BaseSettings, AnyUrl
from typing import Optional


class Settings(BaseSettings):
    DATABASE_URL: AnyUrl
    REDIS_URL: str
    SECRET_KEY: str
    S3_ENDPOINT: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_BUCKET: str
    CORS_ORIGINS: Optional[str] = "*"
    # Railway provides PORT env var
    PORT: int = 8000

    class Config:
        env_file = ".env"


settings = Settings()
