from app.models.rag import RetrievedChunk

DEFAULT_MAX_CONTEXT_CHARS = 5000


def apply_context_budget(
    chunks: list[RetrievedChunk],
    max_chars: int = DEFAULT_MAX_CONTEXT_CHARS,
) -> list[RetrievedChunk]:
    selected: list[RetrievedChunk] = []

    used = 0

    for chunk in chunks:
        size = len(chunk.content)

        if used + size > max_chars:
            continue

        selected.append(chunk)
        used += size

    return selected