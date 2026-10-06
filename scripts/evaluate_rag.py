from app.evaluation.runner import (
    load_dataset,
)
from app.services.rag import RagService


def main() -> None:
    dataset = load_dataset()

    service = RagService()

    passed = 0

    print()
    print("=" * 80)
    print("RAG ANSWER EVALUATION")
    print("=" * 80)

    for case in dataset:
        response = service.answer(
            case.question
        )

        answer_lower = (
            response.answer.lower()
        )

        if case.answerable:
            terms_found = all(
                term.lower()
                in answer_lower
                for term in case.expected_terms
            )

            success = (
                response.grounded
                and terms_found
            )

        else:
            success = (
                not response.grounded
                or "don't have enough information"
                in answer_lower
            )

        if success:
            passed += 1

        status = (
            "PASS"
            if success
            else "FAIL"
        )

        print()
        print(
            f"{status} | {case.id}"
        )

        print(
            f"Question: {case.question}"
        )

        print(
            f"Answer: {response.answer}"
        )

    total = len(dataset)

    score = (
        passed / total
        if total
        else 0.0
    )

    print()
    print("=" * 80)

    print(
        f"Passed: {passed}/{total}"
    )

    print(
        f"Score: {score:.2%}"
    )


if __name__ == "__main__":
    main()