import json
from pathlib import Path

from app.evaluation.models import (
    RetrievalEvaluationCase,
    RetrievalEvaluationResult,
)
from app.evaluation.retrieval import (
    hit_at_k,
    reciprocal_rank,
)
from app.services.retriever import RetrieverService

DATASET_PATH = Path(
    "evaluation/retrieval_dataset.json"
)


def load_dataset() -> list[RetrievalEvaluationCase]:
    raw = json.loads(
        DATASET_PATH.read_text(
            encoding="utf-8"
        )
    )

    return [
        RetrievalEvaluationCase.model_validate(
            item
        )
        for item in raw
    ]


def evaluate() -> list[RetrievalEvaluationResult]:
    dataset = load_dataset()

    retriever = RetrieverService()

    results: list[RetrievalEvaluationResult] = []

    for case in dataset:
        chunks = retriever.retrieve(
            case.question
        )

        hit = hit_at_k(
            chunks,
            case.expected_sources,
        )

        rr = reciprocal_rank(
            chunks,
            case.expected_sources,
        )

        result = RetrievalEvaluationResult(
            id=case.id,
            question=case.question,
            retrieved_sources=[
                chunk.source
                for chunk in chunks
            ],
            hit_at_k=hit,
            reciprocal_rank=rr,
            passed=hit == 1.0,
        )

        results.append(result)

    return results