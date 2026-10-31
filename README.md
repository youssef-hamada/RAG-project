# Company Policies RAG Assistant

A Retrieval-Augmented Generation (RAG) app that answers questions about a corpus of
company policies & procedures with citations.

## Quick start

See full instructions in the final README (added later).

# Corpus

Six synthetic company policy documents used for demo and evaluation.
doc_ids match filenames (without extension).

# Company Policies RAG Assistant

A Retrieval-Augmented Generation (RAG) LLM application that answers user questions
about a corpus of company policies & procedures. Every answer is grounded in the
indexed documents and includes citations to the specific source documents.

## Features

- Ingests PDF / Markdown / TXT policy documents
- Deterministic chunking with overlap
- Local embeddings (`sentence-transformers/all-MiniLM-L6-v2`)
- Persistent vector store (Chroma)
- Top-k retrieval + LLM answer via Groq (`llama-3.1-8b-instant`)
- Guardrails: refuses off-corpus questions, limits output length, always cites sources
- Streamlit chat UI (`/`) and FastAPI JSON API (`/chat`, `/health`)
- GitHub Actions CI (install + import check + pytest)
- Reproducible evaluation: groundedness, citation accuracy, latency p50/p95

## Repository layout

├── data/raw/ # corpus (PDFs / MD / TXT)
├── src/
│ ├── config.py # constants, paths, seeds
│ ├── ingestion/ # loaders, chunker, embedder + Chroma indexer
│ ├── retrieval/ # top-k retriever
│ ├── generation/ # prompt, LLM client, RAG orchestrator, guardrails
│ └── app/ # Streamlit UI + FastAPI
├── scripts/build_index.py # one-shot index build
├── eval/ # questions.jsonl + run_eval.py + results.json
├── tests/ # pytest
└── .github/workflows/ci.yml

Supporting docs:

- [`design-and-evaluation.md`](./design-and-evaluation.md) — architecture, design decisions, evaluation results
- [`ai-tooling.md`](./ai-tooling.md) — AI tools used and how

---

## Requirements

- Python **3.11** or **3.12**
- A free **Groq API key** — https://console.groq.com/keys

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/youssef-hamada/RAG-project.git
cd RAG-project
```
