from pathlib import Path

from app.db.init_db import init_database
from app.db.session import SessionLocal
from app.ingestion.loader import load_documents
from app.ingestion.service import IngestionService

DOCUMENT_DIRECTORY = Path("documents")


def main() -> None:
    init_database()

    documents = load_documents(DOCUMENT_DIRECTORY)

    with SessionLocal() as session:
        service = IngestionService(session)

        for document in documents:
            action = service.ingest(document)

            print(f"{action:8} {document.source}")


if __name__ == "__main__":
    main()
