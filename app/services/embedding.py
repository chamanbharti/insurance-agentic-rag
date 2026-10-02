from langchain_core.embeddings import Embeddings

from app.llm.embeddings import create_embedding_model


class EmbeddingService:
    def __init__(
        self,
        embedding_model: Embeddings | None = None,
    ) -> None:
        self._embedding_model = embedding_model or create_embedding_model()

    def embed_query(self, text: str) -> list[float]:
        return self._embedding_model.embed_query(text)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self._embedding_model.embed_documents(texts)
