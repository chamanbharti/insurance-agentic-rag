from app.models.query_decision import (
    QueryDecision,
    QueryDecisionType,
)
from app.services.domain_gate import has_insurance_terms


class QueryUnderstandingService:
    def __init__(
        self,
        semantic_threshold: float = 0.55,
        retrieval_threshold: float = 0.40,
    ) -> None:
        if not 0 <= retrieval_threshold <= 1:
            raise ValueError("Invalid retrieval threshold")

        if not 0 <= semantic_threshold <= 1:
            raise ValueError("Invalid semantic threshold")

        self.semantic_threshold = semantic_threshold
        self.retrieval_threshold = retrieval_threshold

    def analyze(
        self,
        question: str,
        top_similarity: float | None,
    ) -> QueryDecision:
        lexical_match = has_insurance_terms(question)

        if top_similarity is None:
            return QueryDecision(
                decision=QueryDecisionType.REJECT,
                reason="NO_CANDIDATES",
                lexical_match=lexical_match,
            )

        semantic_match = top_similarity >= self.semantic_threshold

        if semantic_match:
            return QueryDecision(
                decision=QueryDecisionType.ACCEPT,
                reason="STRONG_SEMANTIC_EVIDENCE",
                lexical_match=lexical_match,
                top_similarity=top_similarity,
                semantic_match=True,
            )

        if lexical_match and top_similarity >= self.retrieval_threshold:
            return QueryDecision(
                decision=QueryDecisionType.ACCEPT,
                reason="LEXICAL_AND_RETRIEVAL_EVIDENCE",
                lexical_match=True,
                top_similarity=top_similarity,
            )

        return QueryDecision(
            decision=QueryDecisionType.REJECT,
            reason="INSUFFICIENT_DOMAIN_EVIDENCE",
            lexical_match=lexical_match,
            top_similarity=top_similarity,
            semantic_match=False,
        )
