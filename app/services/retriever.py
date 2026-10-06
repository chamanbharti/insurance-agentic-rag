from app.db.session import SessionLocal
from app.models.rag import RetrievedChunk
from app.repositories.document import DocumentRepository
from app.services.embedding import EmbeddingService

DEFAULT_CANDIDATE_K = 10
DEFAULT_CONTEXT_K = 4
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
        top_k: int = DEFAULT_CONTEXT_K,
        min_similarity: float = DEFAULT_MIN_SIMILARITY,
    ) -> list[RetrievedChunk]:
        query_embedding = self._embedding_service.embed_query(
            question
        )

        with SessionLocal() as session:
            repository = DocumentRepository(session)

            results = repository.similarity_search_with_score(
                query_embedding,
                limit=DEFAULT_CANDIDATE_K,
            )

            candidates: list[RetrievedChunk] = []

            for chunk, distance in results:
                similarity = 1 - distance

                if similarity < min_similarity:
                    continue

                metadata = chunk.chunk_metadata

                candidates.append(
                    RetrievedChunk(
                        content=chunk.content,
                        source=metadata["source"],
                        title=metadata["title"],
                        document_type=metadata[
                            "document_type"
                        ],
                        version=metadata["version"],
                        chunk_index=chunk.chunk_index,
                        similarity=similarity,
                    )
                )

            deduplicated = self._deduplicate(
                candidates
            )

            ranked = self._rerank(
                question,
                deduplicated,
            )

            return ranked[:top_k]

    def _deduplicate(
        self,
        chunks: list[RetrievedChunk],
    ) -> list[RetrievedChunk]:
        seen: set[str] = set()
        result: list[RetrievedChunk] = []

        for chunk in chunks:
            normalized = " ".join(
                chunk.content.lower().split()
            )

            if normalized in seen:
                continue

            seen.add(normalized)
            result.append(chunk)

        return result

    def _rerank(
        self,
        question: str,
        chunks: list[RetrievedChunk],
    ) -> list[RetrievedChunk]:
        query_terms = set(
            question.lower().split()
        )

        def score(
            chunk: RetrievedChunk,
        ) -> float:
            content_terms = set(
                chunk.content.lower().split()
            )

            lexical_overlap = len(
                query_terms & content_terms
            )

            return (
                chunk.similarity
                + lexical_overlap * 0.01
            )

        return sorted(
            chunks,
            key=score,
            reverse=True,
        )