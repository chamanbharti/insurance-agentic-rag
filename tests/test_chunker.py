from pathlib import Path

from app.ingestion.chunker import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    chunk_document,
)
from app.ingestion.models import LoadedDocument


def test_chunk_document() -> None:
    content = "# Test Policy\n\n" + ("Insurance coverage information. " * 100)

    document = LoadedDocument(
        source="test.md",
        title="Test Policy",
        document_type="test",
        version="1.0",
        content=content,
        path=Path("test.md"),
    )

    chunks = chunk_document(document)

    assert len(chunks) > 1

    assert chunks[0].chunk_index == 0

    assert all(chunk.content for chunk in chunks)


def test_chunk_configuration() -> None:
    assert CHUNK_SIZE == 800
    assert CHUNK_OVERLAP == 120
    assert CHUNK_OVERLAP < CHUNK_SIZE
