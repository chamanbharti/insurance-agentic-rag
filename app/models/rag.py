from pydantic import BaseModel, Field


class RetrievedChunk(BaseModel):
    content: str

    source: str

    title: str

    document_type: str

    version: str

    chunk_index: int

    similarity: float


class RagSource(BaseModel):
    source: str

    title: str

    version: str

    chunk_index: int

    similarity: float


class RagRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=2000,
    )


class RagResponse(BaseModel):
    answer: str

    sources: list[RagSource]

    grounded: bool