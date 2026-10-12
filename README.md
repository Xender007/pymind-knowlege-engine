# PyMind

A RAG (retrieval-augmented generation) system implemented from scratch in Python as a learning project: chunking, inverted index and BM25, vector search, fusion, reranking, context building, and evaluation. See `ROADMAP.md` for the plan and `LEDGER.md` for progress.

## Requirements

- Python 3.14
- [uv](https://docs.astral.sh/uv/getting-started/installation/) 0.13 or newer

## Setup

From the repository root:

```powershell
uv sync
```

This creates `.venv` with Python 3.14 (from `.python-version`), installs the dev tools, and installs `pymind` in editable mode.

## Run checks

```powershell
uv run pytest                  # tests
uv run pytest --cov            # tests with coverage
uv run ruff check              # lint
uv run ruff format --check     # formatting
uv run mypy                    # type checking
```

## Layout

```
src/pymind/   package source
tests/        pytest tests
pyproject.toml  project metadata, dependencies, tool config
uv.lock       locked dependency versions
```
