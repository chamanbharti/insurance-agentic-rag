from app.evaluation.runner import evaluate


def main() -> None:
    results = evaluate()

    total = len(results)

    hits = sum(
        result.hit_at_k
        for result in results
    )

    reciprocal_ranks = sum(
        result.reciprocal_rank
        for result in results
    )

    print()
    print("=" * 80)
    print("RETRIEVAL EVALUATION")
    print("=" * 80)

    for result in results:
        status = (
            "PASS"
            if result.passed
            else "FAIL"
        )

        print()
        print(
            f"{status:4} | {result.id}"
        )

        print(
            f"Question: {result.question}"
        )

        print(
            "Retrieved:",
            result.retrieved_sources,
        )

        print(
            "Hit@K:",
            result.hit_at_k,
        )

        print(
            "RR:",
            round(
                result.reciprocal_rank,
                4,
            ),
        )

    hit_rate = (
        hits / total
        if total
        else 0.0
    )

    mrr = (
        reciprocal_ranks / total
        if total
        else 0.0
    )

    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)

    print(
        f"Cases: {total}"
    )

    print(
        f"Hit@K: {hit_rate:.4f}"
    )

    print(
        f"MRR:   {mrr:.4f}"
    )


if __name__ == "__main__":
    main()