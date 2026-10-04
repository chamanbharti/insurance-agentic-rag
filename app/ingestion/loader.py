from pathlib import Path

from app.ingestion.models import LoadedDocument

DOCUMENT_CONFIG: dict[str, dict[str, str]] = {
    "motor-policy.md": {
        "document_type": "motor_policy",
        "version": "1.0",
    },
    "health-policy.md": {
        "document_type": "health_policy",
        "version": "1.0",
    },
    "claim-process.md": {
        "document_type": "claim_process",
        "version": "1.0",
    },
    "refund-policy.md": {
        "document_type": "refund_policy",
        "version": "1.0",
    },
}


def extract_title(content: str) -> str:
    for line in content.splitlines():
        stripped = line.strip()

        if stripped.startswith("# "):
            return stripped.removeprefix("# ").strip()

    raise ValueError("Document does not contain an H1 title.")


def load_document(path: Path) -> LoadedDocument:
    config = DOCUMENT_CONFIG.get(path.name)

    if config is None:
        raise ValueError(f"Unsupported document: {path.name}")

    content = path.read_text(encoding="utf-8").strip()

    if not content:
        raise ValueError(f"Document is empty: {path}")

    return LoadedDocument(
        source=path.name,
        title=extract_title(content),
        document_type=config["document_type"],
        version=config["version"],
        content=content,
        path=path,
    )


def load_documents(
    directory: Path,
) -> list[LoadedDocument]:
    documents: list[LoadedDocument] = []

    for filename in sorted(DOCUMENT_CONFIG):
        path = directory / filename

        if not path.exists():
            raise FileNotFoundError(f"Required document not found: {path}")

        documents.append(load_document(path))

    return documents
