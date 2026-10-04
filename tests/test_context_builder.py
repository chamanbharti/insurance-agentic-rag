from app.models.rag import RetrievedChunk
from app.services.context_builder import (
    build_context,
)


def test_build_context() -> None:
    chunks = [
        RetrievedChunk(
            content="Cancellation is allowed.",
            source="motor-policy.md",
            title="Motor Insurance Policy",
            document_type="motor_policy",
            version="1.0",
            chunk_index=3,
            similarity=0.91,
        )
    ]

    context = build_context(chunks)

    assert "[SOURCE 1]" in context
    assert "motor-policy.md" in context
    assert "Motor Insurance Policy" in context
    assert "Cancellation is allowed." in context