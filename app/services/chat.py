from langchain_core.language_models.chat_models import (
    BaseChatModel,
)
from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
)

from app.llm.ollama import create_chat_model


class ChatService:
    def __init__(
        self,
        chat_model: BaseChatModel | None = None,
    ) -> None:
        self._chat_model = (
            chat_model
            or create_chat_model()
        )

    def chat(
        self,
        message: str,
    ) -> str:
        response = self._chat_model.invoke(
            [
                HumanMessage(
                    content=message
                )
            ]
        )

        return str(response.content)

    def invoke(
        self,
        messages: list[BaseMessage],
    ) -> str:
        response = self._chat_model.invoke(
            messages
        )

        return str(response.content)