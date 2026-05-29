from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./golpeao.db"
    SECRET_KEY: str = "change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    ADMIN_SECRET: str = "admin-secret"
    ENVIRONMENT: str = "development"
    API_BASE_URL: str = "http://localhost:8000"
    DISPLAY_TIMEZONE: str = "America/Recife"

    model_config = {"env_file": ".env"}


settings = Settings()
