from pydantic import BaseModel


class RetrievalDebugInfo(BaseModel):
    accepted: bool

    reason: str

    top_similarity: float | None

    returned_chunks: int