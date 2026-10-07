from app.services.domain_gate import (
    is_insurance_query,
)


def test_motor_query_is_insurance() -> None:
    assert is_insurance_query(
        "Can I cancel my motor insurance?"
    )


def test_health_claim_is_insurance() -> None:
    assert is_insurance_query(
        "What documents are required "
        "for a health claim?"
    )


def test_java_query_is_not_insurance() -> None:
    assert not is_insurance_query(
        "What is the difference between "
        "Java threads and virtual threads?"
    )


def test_geography_query_is_not_insurance() -> None:
    assert not is_insurance_query(
        "What is the capital of France?"
    )