from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Real-Time Pipeline API"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./data/pipeline.db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()