from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
)

from app.models.rag import (
    RagResponse,
    RagSource,
)
from app.prompts.rag import SYSTEM_PROMPT
from app.services.chat import ChatService
from app.services.context_budget import (
    apply_context_budget,
)
from app.services.context_builder import (
    build_context,
)
from app.services.retriever import (
    RetrieverService,
)

NO_CONTEXT_ANSWER = (
    "I don't have enough information in the "
    "available insurance documents to answer "
    "that question."
)


class RagService:
    def __init__(
        self,
        retriever: RetrieverService | None = None,
        chat_service: ChatService | None = None,
    ) -> None:
        self._retriever = (
            retriever
            or RetrieverService()
        )

        self._chat_service = (
            chat_service
            or ChatService()
        )

    def answer(
        self,
        question: str,
    ) -> RagResponse:
        retrieved_chunks = self._retriever.retrieve(
            question
        )

        chunks = apply_context_budget(
            retrieved_chunks
        )

        if not chunks:
            return RagResponse(
                answer=NO_CONTEXT_ANSWER,
                sources=[],
                grounded=False,
            )

        context = build_context(
            chunks
        )

        user_prompt = (
            "INSURANCE CONTEXT:\n\n"
            f"{context}\n\n"
            "USER QUESTION:\n"
            f"{question}\n\n"
            "Answer using only the insurance "
            "context above."
        )

        answer = self._chat_service.invoke(
            [
                SystemMessage(
                    content=SYSTEM_PROMPT
                ),
                HumanMessage(
                    content=user_prompt
                ),
            ]
        )

        sources = [
            RagSource(
                source=chunk.source,
                title=chunk.title,
                version=chunk.version,
                chunk_index=(
                    chunk.chunk_index
                ),
                similarity=(
                    chunk.similarity
                ),
            )
            for chunk in chunks
        ]

        return RagResponse(
            answer=answer,
            sources=sources,
            grounded=True,
        )