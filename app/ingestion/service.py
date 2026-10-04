from sqlalchemy.orm import Session

from app.db.models import (
    Document,
    DocumentChunk,
)
from app.ingestion.chunker import chunk_document
from app.ingestion.models import LoadedDocument
from app.repositories.document import DocumentRepository
from app.services.embedding import EmbeddingService
from app.utils.hashing import sha256_text


class IngestionService:
    def __init__(
        self,
        session: Session,
        embedding_service: EmbeddingService | None = None,
    ) -> None:
        self._session = session

        self._repository = DocumentRepository(session)

        self._embedding_service = embedding_service or EmbeddingService()

    def ingest(
        self,
        loaded_document: LoadedDocument,
    ) -> str:
        document_hash = sha256_text(loaded_document.content)

        existing = self._repository.find_by_source(loaded_document.source)

        if existing is not None and existing.content_hash == document_hash:
            return "SKIPPED"

        chunks = chunk_document(loaded_document)

        chunk_contents = [chunk.content for chunk in chunks]

        embeddings = self._embedding_service.embed_documents(chunk_contents)

        if len(embeddings) != len(chunks):
            raise RuntimeError("Embedding count does not match chunk count.")

        if existing is None:
            document = Document(
                source=loaded_document.source,
                title=loaded_document.title,
                document_type=(loaded_document.document_type),
                version=loaded_document.version,
                content_hash=document_hash,
            )

            self._repository.save_document(document)

            self._session.flush()

            action = "CREATED"

        else:
            document = existing

            document.title = loaded_document.title

            document.document_type = loaded_document.document_type

            document.version = loaded_document.version

            document.content_hash = document_hash

            self._repository.delete_chunks(document)

            self._session.flush()

            action = "UPDATED"

        for chunk, embedding in zip(
            chunks,
            embeddings,
            strict=True,
        ):
            document_chunk = DocumentChunk(
                document_id=document.id,
                chunk_index=chunk.chunk_index,
                content=chunk.content,
                content_hash=sha256_text(chunk.content),
                chunk_metadata={
                    "source": loaded_document.source,
                    "title": loaded_document.title,
                    "document_type": (loaded_document.document_type),
                    "version": loaded_document.version,
                },
                embedding=embedding,
            )

            self._session.add(document_chunk)

        self._session.commit()

        return action
