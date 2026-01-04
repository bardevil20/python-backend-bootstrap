from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_env: str = "local"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/postgres"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()