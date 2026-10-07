from langchain_core.messages import BaseMessage

from app.models.rag import (
    RetrievalResult,
    RetrievedChunk,
)
from app.services.rag import (
    NO_CONTEXT_ANSWER,
    RagService,
)


class FakeRetriever:
    def __init__(
        self,
        chunks: list[RetrievedChunk],
    ) -> None:
        self._chunks = chunks

    def retrieve(
        self,
        question: str,
        top_k: int = 5,
        min_similarity: float = 0.40,
    ) -> RetrievalResult:
        if not self._chunks:
            return RetrievalResult(
                chunks=[],
                accepted=False,
                reason="NO_CANDIDATES",
            )

        return RetrievalResult(
            chunks=self._chunks,
            accepted=True,
            reason="ACCEPTED",
            top_similarity=(
                self._chunks[0].similarity
            ),
        )


class FakeChatService:
    def __init__(
        self,
        answer: str,
    ) -> None:
        self._answer = answer

    def invoke(
        self,
        messages: list[BaseMessage],
    ) -> str:
        return self._answer


def test_rag_returns_no_context_answer() -> None:
    service = RagService(
        retriever=FakeRetriever([]),  # type: ignore[arg-type]
        chat_service=FakeChatService(
            "unused"
        ),  # type: ignore[arg-type]
    )

    response = service.answer(
        "Unknown question"
    )

    assert response.answer == NO_CONTEXT_ANSWER
    assert response.grounded is False
    assert response.sources == []


def test_rag_returns_grounded_answer() -> None:
    chunks = [
        RetrievedChunk(
            content=(
                "Motor policies may be cancelled "
                "within 15 calendar days."
            ),
            source="motor-policy.md",
            title="Motor Insurance Policy",
            document_type="motor_policy",
            version="1.0",
            chunk_index=4,
            similarity=0.88,
        )
    ]

    service = RagService(
        retriever=FakeRetriever(
            chunks
        ),  # type: ignore[arg-type]
        chat_service=FakeChatService(
            "Cancellation is allowed within 15 days."
        ),  # type: ignore[arg-type]
    )

    response = service.answer(
        "Can I cancel my policy?"
    )

    assert response.grounded is True

    assert (
        response.answer
        == "Cancellation is allowed within 15 days."
    )

    assert len(response.sources) == 1

    assert (
        response.sources[0].source
        == "motor-policy.md"
    )