from typing import Annotated

from fastapi import APIRouter, Depends

from app.models.chat import ChatRequest, ChatResponse
from app.services.chat import ChatService

router = APIRouter(
    prefix="/api/v1/chat",
    tags=["Chat"],
)


def get_chat_service() -> ChatService:
    return ChatService()


@router.post(
    "",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
    service: Annotated[ChatService, Depends(get_chat_service)],
) -> ChatResponse:
    return service.chat(request.message)
