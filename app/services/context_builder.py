from app.models.rag import RetrievedChunk


def build_context(
    chunks: list[RetrievedChunk],
) -> str:
    sections: list[str] = []

    for index, chunk in enumerate(
        chunks,
        start=1,
    ):
        section = (
            f"[SOURCE {index}]\n"
            f"File: {chunk.source}\n"
            f"Title: {chunk.title}\n"
            f"Version: {chunk.version}\n"
            f"Chunk: {chunk.chunk_index}\n"
            f"\n"
            f"{chunk.content}"
        )

        sections.append(section)

    return "\n\n---\n\n".join(
        sections
    )