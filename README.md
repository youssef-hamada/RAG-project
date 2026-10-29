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
