from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import DocumentChunk


class DocumentRepository:
    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def similarity_search(
        self,
        query_embedding: list[float],
        limit: int = 3,
    ) -> list[DocumentChunk]:
        statement = (
            select(DocumentChunk)
            .order_by(DocumentChunk.embedding.cosine_distance(query_embedding))
            .limit(limit)
        )

        return list(self._session.scalars(statement))

    def similarity_search_with_score(
        self,
        query_embedding: list[float],
        limit: int = 3,
    ) -> list[tuple[DocumentChunk, float]]:
        distance = DocumentChunk.embedding.cosine_distance(query_embedding)
        statement = (
            select(
                DocumentChunk,
                distance.label("distance"),
            )
            .order_by(distance)
            .limit(limit)
        )
        rows = self._session.execute(statement).all()
        return [(document, float(score)) for document, score in rows]
