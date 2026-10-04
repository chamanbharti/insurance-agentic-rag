from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)

from app.ingestion.models import (
    LoadedDocument,
    TextChunk,
)

CHUNK_SIZE = 800
CHUNK_OVERLAP = 120


def create_text_splitter() -> RecursiveCharacterTextSplitter:
    return RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=[
            "\n## ",
            "\n### ",
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )


def chunk_document(
    document: LoadedDocument,
) -> list[TextChunk]:
    splitter = create_text_splitter()

    texts = splitter.split_text(document.content)

    return [
        TextChunk(
            chunk_index=index,
            content=text.strip(),
        )
        for index, text in enumerate(texts)
        if text.strip()
    ]
