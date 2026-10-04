from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.api.health import router as health_router
from app.api.rag import router as rag_router


def create_app() -> FastAPI:
    application = FastAPI(
        title="Insurance Agentic RAG",
        description=(
            "Production-style Agentic RAG API using FastAPI, LangGraph, Ollama, Redis and pgvector."
        ),
        version="0.2.0",
    )

    application.include_router(health_router)
    application.include_router(chat_router)
    application.include_router(rag_router)

    return application


app = create_app()
