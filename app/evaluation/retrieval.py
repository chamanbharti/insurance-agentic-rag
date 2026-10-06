from app.models.rag import RetrievedChunk


def hit_at_k(
    chunks: list[RetrievedChunk],
    expected_sources: list[str],
) -> float:
    if not expected_sources:
        return 1.0 if not chunks else 0.0

    retrieved_sources = {
        chunk.source
        for chunk in chunks
    }

    return (
        1.0
        if any(
            source in retrieved_sources
            for source in expected_sources
        )
        else 0.0
    )

def reciprocal_rank(
    chunks: list[RetrievedChunk],
    expected_sources: list[str],
) -> float:
    if not expected_sources:
        return 1.0 if not chunks else 0.0

    expected = set(
        expected_sources
    )

    for rank, chunk in enumerate(
        chunks,
        start=1,
    ):
        if chunk.source in expected:
            return 1.0 / rank

    return 0.0