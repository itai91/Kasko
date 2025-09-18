from functools import lru_cache
from pydantic import BaseSettings, AnyUrl
from typing import List


class Settings(BaseSettings):
    # Core
    APP_ENV: str = "development"

    # Mongo
    MONGO_URI: AnyUrl | str = "mongodb://localhost:27017"
    MONGO_DB: str = "kasko"

    # Celery / RabbitMQ
    CELERY_BROKER_URL: str = "amqp://guest:guest@localhost:5672//"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    ENABLE_CELERY: bool = True

    # Redis (rate limit/cache) – reserved for future use
    REDIS_URL: str = "redis://localhost:6379/0"

    # CORS
    CORS_ALLOW_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> "Settings":
    return Settings()


settings = get_settings()

