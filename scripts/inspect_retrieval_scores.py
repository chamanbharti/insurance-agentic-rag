from app.services.embedding import EmbeddingService
from app.repositories.document import DocumentRepository
from app.db.session import SessionLocal

EVALUATION_CASES = [
    {
        "id": "motor-cancel-001",
        "question": "Can I cancel my motor insurance within 15 days?",
        "answerable": True,
    },
    {
        "id": "motor-refund-001",
        "question": (
            "Will I get a full refund if I cancel my motor "
            "policy within 15 days and have not made a claim?"
        ),
        "answerable": True,
    },
    {
        "id": "motor-deductible-001",
        "question": "What is the deductible for a motor own-damage claim?",
        "answerable": True,
    },
    {
        "id": "health-ambulance-001",
        "question": "What is the ambulance coverage limit?",
        "answerable": True,
    },
    {
        "id": "health-waiting-001",
        "question": ("What is the initial waiting period for non-accidental hospitalization?"),
        "answerable": True,
    },
    {
        "id": "health-documents-001",
        "question": ("Which documents are required for a health reimbursement claim?"),
        "answerable": True,
    },
    {
        "id": "claim-status-001",
        "question": "What are the possible insurance claim statuses?",
        "answerable": True,
    },
    {
        "id": "refund-time-001",
        "question": "How long does an approved insurance refund take?",
        "answerable": True,
    },
    {
        "id": "ood-france-001",
        "question": "What is the capital of France?",
        "answerable": False,
    },
    {
        "id": "ood-java-001",
        "question": "Explain Java virtual threads.",
        "answerable": False,
    },
]

CANDIDATE_K = 15


def main() -> None:
    embedding_service = EmbeddingService()

    with SessionLocal() as session:
        repository = DocumentRepository(session)

        for case in EVALUATION_CASES:
            case_id = str(case["id"])
            question = str(case["question"])
            answerable = bool(case["answerable"])

            print()
            print("=" * 80)
            print(f"{case_id} | answerable={answerable}")
            print(question)
            print("-" * 80)

            query_embedding = embedding_service.embed_query(question)

            rows = repository.similarity_search_with_score(
                query_embedding=query_embedding,
                limit=CANDIDATE_K,
            )

            if not rows:
                print("No candidates retrieved.")
                continue

            for rank, (chunk, distance) in enumerate(
                rows,
                start=1,
            ):
                similarity = 1.0 - float(distance)

                document = chunk.document

                print(
                    f"{rank:02d}. "
                    f"similarity={similarity:.4f} "
                    f"source={document.source} "
                    f"chunk={chunk.chunk_index}"
                )

    print()
    print("=" * 80)
    print("INSPECTION COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
