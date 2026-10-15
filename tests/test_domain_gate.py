from app.services.domain_gate import (
    has_insurance_terms,
)


def test_motor_query_is_insurance() -> None:
    assert has_insurance_terms("Can I cancel my motor insurance?")


def test_health_claim_is_insurance() -> None:
    assert has_insurance_terms("What documents are required for a health claim?")


def test_java_query_is_not_insurance() -> None:
    assert not has_insurance_terms(
        "What is the difference between Java threads and virtual threads?"
    )


def test_geography_query_is_not_insurance() -> None:
    assert not has_insurance_terms("What is the capital of France?")
