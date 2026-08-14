"""Configuração centralizada da API."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    mongo_uri: str = "mongodb://chatterbox:chatterbox@mongo:27017"
    mongo_db_name: str = "chatterbox"

    ai_provider: str = "anthropic"
    ai_api_key: str = "changeme"
    ai_model: str = "gemini-3.5-flash"
    ai_system_goal: str = "Convencer o usuário que a Terra é plana."
    gcp_project_id: str = "teste"
    gcp_region: str = "global"

    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


settings = Settings()
