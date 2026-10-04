from fastapi import APIRouter

from app.models.rag import (
    RagRequest,
    RagResponse,
)
from app.services.rag import RagService

# from app.services.rag import RagService

router = APIRouter(
    prefix="/api/v1/rag",
    tags=["rag"],
)


@router.post(
    "/ask",
    response_model=RagResponse,
)
def ask(
    request: RagRequest,
) -> RagResponse:
    service = RagService()

    return service.answer(
        request.question
    )