from app.evaluation.runner import (
    load_dataset,
)
from app.services.retriever import (
    RetrieverService,
)


def main() -> None:
    dataset = load_dataset()

    retriever = RetrieverService()

    for case in dataset:
        chunks = retriever.retrieve(
            case.question,
            min_similarity=-1.0,
        )

        print()
        print("=" * 80)

        print(
            case.id,
            "| answerable=",
            case.answerable,
        )

        print(case.question)

        for rank, chunk in enumerate(
            chunks,
            start=1,
        ):
            print(
                f"{rank}. "
                f"{chunk.similarity:.4f} "
                f"{chunk.source}"
            )


if __name__ == "__main__":
    main()