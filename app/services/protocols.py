from typing import Protocol

from langchain_core.messages import BaseMessage

from app.models.rag import RetrievedChunk


class RetrieverProtocol(Protocol):
    def retrieve(
        self,
        question: str,
        top_k: int = 5,
        min_similarity: float = 0.40,
    ) -> list[RetrievedChunk]:
        ...


class ChatProtocol(Protocol):
    def invoke(
        self,
        messages: list[BaseMessage],
    ) -> str:
        ...