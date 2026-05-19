from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BACKEND_URL: str = "http://localhost:8000"
    REDIS_URL: str = "redis://localhost:6379/1"
    RATE_LIMIT_PER_MINUTE: int = 60
    API_PREFIX: str = "/api/v1"

    model_config = {"env_file": ".env"}


settings = Settings()
