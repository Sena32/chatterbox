"""
Configuração centralizada da API.

Estado: PLACEHOLDER (boilerplate)
Spec de referência: specs/002-ia-responde-com-objetivo/plan.md (seção core/config.py)

TODO (task T1 da spec 002):
  - Preencher todos os campos de Settings usando pydantic-settings
  - Expor instância singleton `settings` usada pelo resto da aplicação
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # --- MongoDB ---
    mongo_uri: str = "mongodb://chatterbox:chatterbox@mongo:27017"
    mongo_db_name: str = "chatterbox"

    # --- IA ---
    ai_provider: str = "anthropic"       # "anthropic" | "openai" | "fake"
    ai_api_key: str = "changeme"
    ai_model: str = "claude-sonnet-4-6"
    ai_system_goal: str = "Convencer o usuário que a Terra é plana."

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Singleton — importar em qualquer módulo via: from src.core.config import settings
settings = Settings()
