from app.evaluation.retrieval import (
    hit_at_k,
    reciprocal_rank,
)
from app.models.rag import RetrievedChunk


def chunk(
    source: str,
) -> RetrievedChunk:
    return RetrievedChunk(
        content="test",
        source=source,
        title="Test",
        document_type="test",
        version="1.0",
        chunk_index=0,
        similarity=0.8,
    )


def test_hit_at_k_found() -> None:
    chunks = [
        chunk("motor-policy.md"),
        chunk("refund-policy.md"),
    ]

    result = hit_at_k(
        chunks,
        ["refund-policy.md"],
    )

    assert result == 1.0


def test_hit_at_k_not_found() -> None:
    chunks = [
        chunk("motor-policy.md")
    ]

    result = hit_at_k(
        chunks,
        ["health-policy.md"],
    )

    assert result == 0.0


def test_reciprocal_rank_first() -> None:
    chunks = [
        chunk("refund-policy.md"),
        chunk("motor-policy.md"),
    ]

    result = reciprocal_rank(
        chunks,
        ["refund-policy.md"],
    )

    assert result == 1.0


def test_reciprocal_rank_second() -> None:
    chunks = [
        chunk("motor-policy.md"),
        chunk("refund-policy.md"),
    ]

    result = reciprocal_rank(
        chunks,
        ["refund-policy.md"],
    )

    assert result == 0.5


def test_ood_hit_when_empty() -> None:
    assert (
        hit_at_k(
            [],
            [],
        )
        == 1.0
    )


def test_ood_fails_when_results_exist() -> None:
    chunks = [
        chunk("motor-policy.md")
    ]

    assert (
        hit_at_k(
            chunks,
            [],
        )
        == 0.0
    )