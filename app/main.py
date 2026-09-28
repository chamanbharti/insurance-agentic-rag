from fastapi import FastAPI

from app.api.health import router as health_router


def create_app() -> FastAPI:
    application = FastAPI(
        title="Insurance Agentic RAG",
        description=(
            "Production-style Agentic RAG API using FastAPI, LangGraph, Ollama, Redis and pgvector."
        ),
        version="0.1.0",
    )

    application.include_router(health_router)

    return application


app = create_app()
