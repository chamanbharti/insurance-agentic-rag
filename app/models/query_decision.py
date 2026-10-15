from enum import StrEnum

from pydantic import BaseModel, Field


class QueryDecisionType(StrEnum):
    ACCEPT = "ACCEPT"
    REJECT = "REJECT"
    CLARIFY = "CLARIFY"


class QueryDecision(BaseModel):
    decision: QueryDecisionType
    reason: str
    lexical_match: bool
    top_similarity: float | None = None
    semantic_match: bool = False
    confidence: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
    )
