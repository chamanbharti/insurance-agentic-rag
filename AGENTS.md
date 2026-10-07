# Repository Guidelines

## Project Structure & Module Organization

The application lives in `app/`; `src/insurance_agentic_rag/` is a minimal package scaffold. FastAPI routes are in `app/api/`, request and response schemas in `app/models/`, and retrieval, context construction, and chat logic in `app/services/`. Keep database models and sessions in `app/db/`, persistence operations in `app/repositories/`, and document loading and chunking in `app/ingestion/`. Prompts live in `app/prompts/`.

Insurance source documents are Markdown files under `documents/`. Evaluation cases live in `evaluation/retrieval_dataset.json`, evaluation logic in `app/evaluation/`, and executable workflows in `scripts/`. Tests live in `tests/`.

## Build, Test, and Development Commands

Use Python 3.12; run from the repository root:

- `uv sync`: install application and development dependencies.
- `docker compose up -d`: start PostgreSQL with pgvector on host port `5433`.
- `uv run uvicorn app.main:app --reload`: run the local API.
- `uv run python -m scripts.ingest`: initialize database tables and ingest `documents/`; requires PostgreSQL and Ollama embeddings.
- `uv run pytest`: run the automated test suite.
- `uv run ruff check .` and `uv run ruff format .`: lint and format Python files.
- `uv run mypy app scripts`: check application and script types in strict mode.
- `uv run python -m scripts.evaluate_retrieval`: report retrieval quality.
- `uv run python -m scripts.evaluate_rag`: evaluate grounded answers; requires ingested documents and Ollama.

## Coding Style & Naming Conventions

Use four-space indentation, type annotations, and a 100-character line limit. Use `snake_case` for modules, functions, and variables; `PascalCase` for classes; and `UPPER_SNAKE_CASE` for constants. Keep routes thin and inject service dependencies where practical.

## Testing Guidelines

Use pytest with `test_*.py` files and `test_*` functions. Follow existing fake retriever, chat, and embedding patterns to avoid external services in unit tests. Cover changed behavior, including missing context and source grounding. No numeric coverage threshold is configured. Run focused tests with `uv run pytest tests/test_rag_service.py`.

## Commit & Pull Request Guidelines

History uses concise messages such as `feat: add grounded insurance RAG pipeline`. Follow that prefix-and-summary pattern. PRs should explain the behavior change, include validation commands and results, and link relevant issues. Document configuration or ingestion changes and include API examples when responses change.

## Security & Configuration Tips

Settings load from `.env` through `app/core/config.py`; `.env.example` is currently empty. Keep credentials out of commits. Local defaults use Ollama at `localhost:11434`, `gemma4:12b` for chat, and `nomic-embed-text` for 768-dimensional embeddings. Coordinate embedding changes with database vector dimensions and document re-ingestion.
