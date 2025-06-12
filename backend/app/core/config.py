from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    cors_origins: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    debug: bool = True

    class Config:
        env_file = ".env"

settings = Settings()
