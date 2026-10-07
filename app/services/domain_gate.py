import re

INSURANCE_TERMS = {
    "insurance",
    "policy",
    "premium",
    "claim",
    "claims",
    "coverage",
    "covered",
    "deductible",
    "refund",
    "hospital",
    "hospitalization",
    "ambulance",
    "motor",
    "vehicle",
    "cashless",
    "reimbursement",
    "insured",
    "insurer",
    "renewal",
    "cancel",
    "cancellation",
}


def tokenize(text: str) -> set[str]:
    return set(
        re.findall(
            r"[a-z0-9]+",
            text.lower(),
        )
    )


def is_insurance_query(
    question: str,
) -> bool:
    tokens = tokenize(question)

    return bool(
        tokens & INSURANCE_TERMS
    )