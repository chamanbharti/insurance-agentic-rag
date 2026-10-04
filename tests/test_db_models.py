from app.db.models import (
    EMBEDDING_DIMENSION,
    Document,
    DocumentChunk,
)


def test_document_table_name() -> None:
    assert Document.__tablename__ == "documents"


def test_document_chunk_table_name() -> None:
    assert DocumentChunk.__tablename__ == "document_chunks"


def test_embedding_dimension() -> None:
    assert EMBEDDING_DIMENSION == 768
