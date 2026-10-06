from pydantic import BaseModel


class RetrievalEvaluationCase(BaseModel):
    id: str

    question: str

    expected_sources: list[str]

    expected_terms: list[str]

    answerable: bool


class RetrievalEvaluationResult(BaseModel):
    id: str

    question: str

    retrieved_sources: list[str]

    hit_at_k: float

    reciprocal_rank: float

    passed: bool