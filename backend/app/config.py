from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "TaskFlow"
    database_url: str = "sqlite:///./taskflow.db"
    jwt_secret: str = "8f3c2a1b9e7d4f6c0a5b2e8d1f4a7c3b6e9d2f5a8c1b4e7d0f3a6c9b2e5d8f1"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24 * 7
    upload_dir: str = "./uploads"
    support_master_password: str = "admin123"
    debug: bool = True
    cors_origins: list[str] = ["*"]

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
