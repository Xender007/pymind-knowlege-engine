# PyMind Roadmap: RAG from Scratch

Dependency-ordered. Each task is small and testable. **Only the current task is detailed** (see "Current task"). Later tasks are detailed when they become current. Significant scope changes are explained and approved before this file changes.

Tooling: Python 3.14.7, uv. No implementation code or pseudocode appears in this plan.

## Rules of engagement
- You write the code; Claude teaches, hints, and reviews (see CLAUDE.md).
- Per task: design (your words) → pseudocode (yours) → implement → hints → review (scored) → fix → re-review.
- A task is complete only with evidence against its acceptance criteria. Status lives in LEDGER.md.
- Educational core is implemented by you. Pretrained models/services only for embeddings and generation.

## Storage architecture (decided 2026-10-13)
- **PostgreSQL is the main database and source of truth** for documents, chunks, metadata, and eval data.
- **No external vector DB, and no pgvector for retrieval.** The inverted index, BM25, and vector index are built by you; they are derived artifacts, rebuildable from Postgres.
- Whether raw embeddings are stored in Postgres or on disk is decided in M3-T6.
- Driver, migrations tool, and Docker-vs-native install are decided in M0-T5, not now.

## Phases and milestones

### M0: Foundations
| ID | Task | Objective |
|---|---|---|
| M0-T1 | Project scaffold | Reproducible uv project: src layout, pyproject, tests, lint, types |
| M0-T2 | Config and logging | Typed settings from env/file; structured logging |
| M0-T3 | Core data models | Document, Chunk, SearchResult types with validation |
| M0-T4 | Test corpus and fixtures | Small deterministic corpus plus shared test fixtures |
| M0-T5 | Postgres setup | Local PostgreSQL, connection config, migrations tool decision, isolated test database |

### M1: Ingestion and chunking
| ID | Task | Objective |
|---|---|---|
| M1-T1 | Document loaders | Load txt/md (then pdf) into Document, with encoding and error handling |
| M1-T2 | Text normalization | Clean whitespace/unicode deterministically |
| M1-T3 | Fixed-size chunker | Size and overlap chunking with boundary edge cases |
| M1-T4 | Structure-aware chunker | Sentence/paragraph/recursive splitting |
| M1-T5 | Chunk metadata and IDs | Stable chunk IDs, source offsets, provenance |
| M1-T6 | Postgres persistence | Schema and repository layer for documents and chunks; transactions, idempotent re-ingest |

### M2: Lexical retrieval
| ID | Task | Objective |
|---|---|---|
| M2-T1 | Tokenizer | Lowercasing, punctuation, stopwords, optional stemming |
| M2-T2 | Inverted index | Term → postings, doc lengths, build and update |
| M2-T3 | TF-IDF scoring | Baseline ranking |
| M2-T4 | BM25 | Parametrized scoring; compare with TF-IDF |
| M2-T5 | Index persistence | Save/load index; versioning; rebuildable from Postgres chunks |
| M2-T6 | Lexical search API | Top-k query interface |

### M3: Dense retrieval
| ID | Task | Objective |
|---|---|---|
| M3-T1 | Embedding adapter | Thin interface over a pretrained embedding model; batching |
| M3-T2 | Similarity math | Cosine/dot, normalization, vectorized with numpy |
| M3-T3 | Brute-force vector index | Exact top-k search |
| M3-T4 | Top-k selection | Heap vs full sort; complexity trade-offs |
| M3-T5 | Approximate index | Implement one ANN idea (e.g. IVF or HNSW-lite); measure recall vs speed |
| M3-T6 | Vector persistence | Save/load vectors and index; decide where raw embeddings live (Postgres vs files) |

### M4: Hybrid retrieval and fusion
| ID | Task | Objective |
|---|---|---|
| M4-T1 | Score normalization | Make lexical and dense scores comparable |
| M4-T2 | Weighted fusion | Tunable linear combination |
| M4-T3 | Reciprocal Rank Fusion | Rank-based fusion |
| M4-T4 | Result merging | Dedupe across chunks and sources |

### M5: Reranking
| ID | Task | Objective |
|---|---|---|
| M5-T1 | Reranker interface | Pluggable reranker contract |
| M5-T2 | MMR | Relevance vs diversity |
| M5-T3 | Cross-encoder reranking | Wrap a pretrained cross-encoder; own the pipeline logic |
| M5-T4 | Rerank evaluation | Measure uplift against M4 baseline |

### M6: Context building and generation
| ID | Task | Objective |
|---|---|---|
| M6-T1 | Token budgeting | Count tokens; fit context window |
| M6-T2 | Context assembly | Order, truncate, deduplicate chunks |
| M6-T3 | Prompt construction | Templates, instructions, citation markers |
| M6-T4 | Generation adapter | Thin LLM client; retries, timeouts, errors |
| M6-T5 | Citations and grounding | Map answer claims to source chunks |

### M7: Evaluation
| ID | Task | Objective |
|---|---|---|
| M7-T1 | Eval dataset | Questions with labelled relevant chunks (stored in Postgres) |
| M7-T2 | Retrieval metrics | Recall@k, MRR, nDCG |
| M7-T3 | Generation checks | Faithfulness and answer-quality heuristics |
| M7-T4 | Ablation harness | Compare chunking/BM25/dense/hybrid/rerank configs |
| M7-T5 | Regression gate | Fail the build when metrics drop |

### M8: Production readiness
| ID | Task | Objective |
|---|---|---|
| M8-T1 | CLI | Ingest, index, query commands |
| M8-T2 | HTTP API | Service wrapper with validation and errors |
| M8-T3 | Caching and performance | Profile; cache embeddings/results |
| M8-T4 | Observability | Metrics, tracing hooks, structured logs |
| M8-T5 | Security and robustness | Input limits, prompt-injection awareness, secrets handling |
| M8-T6 | Packaging and docs | Reproducible install, README, architecture notes |

## Current task: M0-T1 Project scaffold

- **Objective:** Reproducible, isolated Python project skeleton that installs, imports, and tests with documented commands.
- **Why:** Every later task depends on correct imports, environments, and test discovery.
- **Prerequisites:** Python 3.14.7 installed; uv installed; git initialized.
- **Functional requirements:**
  - Isolated virtual environment, not committed.
  - One declarative project config file (metadata, Python constraint, runtime vs dev dependencies).
  - `src/`-layout package importable after an editable install.
  - `tests/` with at least one passing smoke test that imports the package.
  - `.gitignore` for venv, caches, build artifacts.
  - README with setup and test instructions using uv.
- **Non-functional requirements:** Fresh-clone setup works from documented commands only; no global installs; tool config lives in the project config file.
- **Constraints and edge cases:** Running tests without installing the package; wrong Python version active; Windows/PowerShell activation differences; deleting and rebuilding the venv gives the same result; lockfile decision.
- **Acceptance criteria:**
  1. Fresh environment plus documented uv commands yields a working setup.
  2. Importing the package works from a directory outside the project.
  3. Test runner discovers and passes the smoke test.
  4. Linter/formatter and type checker run clean on the empty package.
  5. `git status` shows no venv or cache files.
- **Suggested tests:** Smoke test importing the package and checking it exposes a version; deliberately break and rebuild the environment.
- **Concepts to research:** venv, `pyproject.toml` (PEP 621), `src` layout vs flat, editable installs, `__init__.py`, pytest discovery, ruff, mypy, uv commands (venv, pip install, sync, run) and lockfiles.
- **Definition of done:** All five criteria demonstrated by you; you can explain why `src` layout prevents accidental imports from the working directory.

## Next step
Send your written scaffold design for review before creating files.
