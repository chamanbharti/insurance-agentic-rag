from langchain_ollama import OllamaEmbeddings

from app.core.config import get_settings


def create_embedding_model() -> OllamaEmbeddings:
    settings = get_settings()

    return OllamaEmbeddings(
        model=settings.ollama_embedding_model, base_url=settings.ollama_base_url
    )
