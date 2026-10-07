from app.db.session import SessionLocal
from app.models.rag import (
    RetrievalResult,
    RetrievedChunk,
)
from app.repositories.document import DocumentRepository
from app.services.domain_gate import (
    is_insurance_query,
)
from app.services.embedding import EmbeddingService

DEFAULT_CANDIDATE_K = 15
DEFAULT_CONTEXT_K = 4
DEFAULT_MIN_SIMILARITY = 0.40
DEFAULT_MAX_CHUNKS_PER_SOURCE = 2


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
    ) -> RetrievalResult:

        if not is_insurance_query(question):
            return RetrievalResult(
                chunks=[],
                accepted=False,
                reason="OUT_OF_DOMAIN",
            )

        candidates = self._retrieve_candidates(
            question
        )

        if not candidates:
            return RetrievalResult(
                chunks=[],
                accepted=False,
                reason="NO_CANDIDATES",
            )

        top_similarity = candidates[0].similarity

        filtered = [
            chunk
            for chunk in candidates
            if chunk.similarity
            >= min_similarity
        ]

        if not filtered:
            return RetrievalResult(
                chunks=[],
                accepted=False,
                reason="LOW_RELEVANCE",
                top_similarity=top_similarity,
            )

        deduplicated = self._deduplicate(
            filtered
        )

        ranked = self._rerank(
            question,
            deduplicated,
        )
        diverse = self._limit_per_source(
            ranked
        )
        return RetrievalResult(
            # chunks=ranked[:top_k],
            chunks=diverse[:top_k],
            accepted=True,
            reason="ACCEPTED",
            top_similarity=top_similarity,
        )

    def _retrieve_candidates(
        self,
        question: str,
    ) -> list[RetrievedChunk]:

        query_embedding = (
            self._embedding_service
            .embed_query(question)
        )

        with SessionLocal() as session:
            repository = DocumentRepository(
                session
            )

            results = (
                repository
                .similarity_search_with_score(
                    query_embedding,
                    limit=DEFAULT_CANDIDATE_K,
                )
            )

            candidates: list[RetrievedChunk] = []

            for chunk, distance in results:
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
                        similarity=1 - distance,
                    )
                )

            return candidates

    def _deduplicate(
        self,
        chunks: list[RetrievedChunk],
    ) -> list[RetrievedChunk]:

        seen: set[str] = set()
        result: list[RetrievedChunk] = []

        for chunk in chunks:
            normalized = " ".join(
                chunk.content
                .lower()
                .split()
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

        question_terms = set(
            question.lower().split()
        )

        def score(
            chunk: RetrievedChunk,
        ) -> float:

            content_terms = set(
                chunk.content.lower().split()
            )

            overlap = len(
                question_terms
                & content_terms
            )

            return (
                chunk.similarity
                + overlap * 0.01
            )

        return sorted(
            chunks,
            key=score,
            reverse=True,
        )

    def _limit_per_source(
        self,
        chunks: list[RetrievedChunk],
        max_per_source: int = DEFAULT_MAX_CHUNKS_PER_SOURCE,
    ) -> list[RetrievedChunk]:

        counts: dict[str, int] = {}
        result: list[RetrievedChunk] = []

        for chunk in chunks:
            count = counts.get(
                chunk.source,
                0,
            )

            if count >= max_per_source:
                continue

            result.append(chunk)

            counts[chunk.source] = count + 1

        return result