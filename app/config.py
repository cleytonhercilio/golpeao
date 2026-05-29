from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./golpeao.db"
    SECRET_KEY: str  # required — no insecure default
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    ADMIN_SECRET: str = "admin-secret"
    ENVIRONMENT: str = "development"
    API_BASE_URL: str = "http://localhost:8000"
    DISPLAY_TIMEZONE: str = "America/Recife"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
