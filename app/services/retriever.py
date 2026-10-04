from app.db.session import SessionLocal
from app.models.rag import RetrievedChunk
from app.repositories.document import DocumentRepository
from app.services.embedding import EmbeddingService

DEFAULT_TOP_K = 5
DEFAULT_MIN_SIMILARITY = 0.40

class RetrieverService:
    def __init__(
        self,
        embedding_service: EmbeddingService | None = None,
    ) -> None:
        self._embedding_service = (
            embedding_service
            or EmbeddingService()
        )

    def retrieve(
        self,
        question: str,
        top_k: int = DEFAULT_TOP_K,
        min_similarity: float = DEFAULT_MIN_SIMILARITY,
    ) -> list[RetrievedChunk]:
        query_embedding = (
            self._embedding_service.embed_query(
                question
            )
        )

        with SessionLocal() as session:
            repository = DocumentRepository(
                session
            )

            results = (
                repository
                .similarity_search_with_score(
                    query_embedding,
                    limit=top_k,
                )
            )

            retrieved: list[RetrievedChunk] = []

            for chunk, distance in results:
                similarity = 1 - distance
                if similarity < min_similarity:
                    continue

                metadata = chunk.chunk_metadata

                retrieved.append(
                    RetrievedChunk(
                        content=chunk.content,
                        source=metadata["source"],
                        title=metadata["title"],
                        document_type=(
                            metadata[
                                "document_type"
                            ]
                        ),
                        version=metadata["version"],
                        chunk_index=(
                            chunk.chunk_index
                        ),
                        similarity= similarity,
                    )
                )

            return retrieved