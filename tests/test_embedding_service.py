from langchain_core.embeddings import FakeEmbeddings

from app.services.embedding import EmbeddingService


def test_embed_query() -> None:
    fake_embeddings = FakeEmbeddings(
        size=4,
    )

    service = EmbeddingService(
        embedding_model=fake_embeddings,
    )

    vector = service.embed_query("motor insurance")

    assert len(vector) == 4


def test_embed_documents() -> None:
    fake_embeddings = FakeEmbeddings(
        size=4,
    )

    service = EmbeddingService(
        embedding_model=fake_embeddings,
    )

    vectors = service.embed_documents(
        [
            "motor insurance",
            "health insurance",
        ]
    )

    assert len(vectors) == 2
    assert all(len(vector) == 4 for vector in vectors)
