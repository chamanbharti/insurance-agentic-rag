from langchain_core.language_models.chat_models import BaseChatModel

from app.core.config import get_settings
from app.llm.ollama import create_chat_model
from app.models.chat import ChatResponse


class ChatService:
    def __init__(
        self,
        chat_model: BaseChatModel | None = None,
    ) -> None:
        self._chat_model = chat_model or create_chat_model()

    def chat(self, message: str) -> ChatResponse:
        settings = get_settings()

        response = self._chat_model.invoke(message)

        return ChatResponse(
            answer=str(response.content),
            model=settings.ollama_chat_model,
        )
