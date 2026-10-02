from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Insurance Agentic RAG"
    app_env: str = "local"

    ollama_base_url: str = "http://localhost:11434"
    ollama_chat_model: str = "gemma4:12b"
    ollama_embedding_model: str = "nomic-embed-text"
    embedding_dimension: int = 768

    database_url: str = "postgresql+psycopg://insurance:insurance@localhost:5433/insurance"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
