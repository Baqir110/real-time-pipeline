from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Real-Time Data Engineering Pipeline"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./data/pipeline.db"  # Defaults to local SQLite for zero-config testing, easily switchable to PostgreSQL

    class Config:
        env_file = ".env"

settings = Settings()