from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "sqlite:///./careerflow.db"
    ai_api_key: str | None = None
    ai_base_url: str | None = None
    cors_origins: str = "http://localhost:3000"
    max_upload_mb: int = 5
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
