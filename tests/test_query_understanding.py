import pytest

from app.models.query_decision import QueryDecisionType
from app.services.query_understanding import (
    QueryUnderstandingService,
)


@pytest.fixture
def service() -> QueryUnderstandingService:
    return QueryUnderstandingService()


def test_explicit_insurance_query(
    service: QueryUnderstandingService,
) -> None:
    result = service.analyze(
        "Can I cancel my motor insurance?",
        top_similarity=0.80,
    )

    assert result.decision == QueryDecisionType.ACCEPT
    assert result.lexical_match is True


def test_implicit_query_with_strong_evidence(
    service: QueryUnderstandingService,
) -> None:
    result = service.analyze(
        "How much do I have to pay myself when my car is damaged?",
        top_similarity=0.72,
    )

    assert result.decision == QueryDecisionType.ACCEPT
    assert result.semantic_match is True


def test_java_out_of_domain(
    service: QueryUnderstandingService,
) -> None:
    result = service.analyze(
        "Explain Java virtual threads.",
        top_similarity=0.4222,
    )

    assert result.decision == QueryDecisionType.REJECT


def test_france_out_of_domain(
    service: QueryUnderstandingService,
) -> None:
    result = service.analyze(
        "What is the capital of France?",
        top_similarity=0.3573,
    )

    assert result.decision == QueryDecisionType.REJECT


def test_no_candidates(
    service: QueryUnderstandingService,
) -> None:
    result = service.analyze(
        "Unknown question",
        top_similarity=None,
    )

    assert result.decision == QueryDecisionType.REJECT


def test_lexical_query_with_weak_retrieval(
    service: QueryUnderstandingService,
) -> None:
    result = service.analyze(
        "Explain insurance concepts",
        top_similarity=0.25,
    )

    assert result.decision == QueryDecisionType.REJECT
