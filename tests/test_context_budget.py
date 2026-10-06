from app.models.rag import RetrievedChunk
from app.services.context_budget import (
    apply_context_budget,
)


def make_chunk(
    content: str,
    index: int,
) -> RetrievedChunk:
    return RetrievedChunk(
        content=content,
        source="test.md",
        title="Test",
        document_type="test",
        version="1.0",
        chunk_index=index,
        similarity=0.8,
    )


def test_context_budget() -> None:
    chunks = [
        make_chunk(
            "A" * 100,
            0,
        ),
        make_chunk(
            "B" * 100,
            1,
        ),
        make_chunk(
            "C" * 100,
            2,
        ),
    ]

    result = apply_context_budget(
        chunks,
        max_chars=210,
    )

    assert len(result) == 2


def test_context_budget_empty() -> None:
    result = apply_context_budget(
        [],
        max_chars=100,
    )

    assert result == []