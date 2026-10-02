# Create the project
mkdir insurance-agentic-rag
cd insurance-agentic-rag

Initialize with uv:
uv init --python 3.12

Remove:
rm main.py

## Create the initial directories:
mkdir -p app/api
mkdir -p tests

touch app/__init__.py
touch app/api/__init__.py
touch tests/__init__.py

## Install FastAPI
uv add "fastapi[standard]"
This will update:
pyproject.toml
uv.lock

## Install development dependencies
Run:
uv add --dev pytest ruff mypy httpx

Verify:
uv tree

## Configure pyproject.toml
Open:
pyproject.toml
Then synchronize:
uv sync

## Run Ruff with --fix  
Let Ruff automatically reorder imports:
uv run ruff check . --fix

#######################
# Insurance Agentic RAG

Production-style Insurance Agentic RAG application.

## Technology Stack

- Python 3.12
- FastAPI
- LangChain
- LangGraph
- Ollama
- PostgreSQL
- pgvector
- Redis
- Docker
- Kubernetes

## Current Status

Checkpoint 1:

- [x] Python project
- [x] uv dependency management
- [x] FastAPI
- [x] Health API
- [x] Ruff
- [x] mypy
- [x] pytest

Upcoming:

- [ ] Ollama
- [ ] Embeddings
- [ ] PostgreSQL + pgvector
- [ ] Document ingestion
- [ ] RAG
- [ ] Redis caching
- [ ] Hybrid retrieval
- [ ] LangGraph agents
- [ ] Observability
- [ ] Evaluation

## Run

```bash
uv sync
uv run uvicorn app.main:app --reload
######################

git branch -m checkpoint-01-fastapi main
git fetch origin
git branch -u origin/main main
git remote set-head origin -a