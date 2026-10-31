# Design & Evaluation

## 1. Architecture Overview

The application follows a standard Retrieval-Augmented Generation (RAG) pipeline, split into four distinct layers to separate concerns and make the codebase maintainable and testable.

**Data Flow:**

1. **Ingestion (`src/ingestion/`)**: Parses raw PDF/TXT/MD documents from `data/raw/`, splits them into overlapping text chunks, and generates dense vector embeddings.
2. **Indexing**: Embeds the chunks using `sentence-transformers/all-MiniLM-L6-v2` and persists them in a local **ChromaDB** vector store. Metadata (document ID, title, source path) is attached to each vector to enable accurate citations.
3. **Retrieval (`src/retrieval/`)**: When a user asks a question, the query is embedded using the same model, and a cosine similarity search retrieves the top-`k` (default 4) most relevant chunks.
4. **Generation (`src/generation/`)**: The retrieved chunks are injected into a prompt alongside the user's query. The prompt is sent to **Groq** (`openai/gpt-oss-20b`), and the generated answer is passed through a guardrails layer before being returned to the user.

## 2. Design Decisions & Rationale

| Component             | Choice                                            | Rationale                                                                                                                                                                                                        |
| :-------------------- | :------------------------------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Embedding Model**   | `sentence-transformers/all-MiniLM-L6-v2`          | Runs locally (no API costs), extremely fast, and performs exceptionally well on short English text/policy retrieval.                                                                                             |
| **Vector Database**   | ChromaDB (local)                                  | Zero-configuration, supports persistent local storage, and easily handles metadata filtering for citations.                                                                                                      |
| **Chunking Strategy** | 700 chars / 120 overlap                           | Roughly 2–3 paragraphs per chunk. Provides enough context for a complete answer without diluting the retrieval with off-topic text. The 120-char overlap ensures facts that straddle boundaries aren't lost.     |
| **Retrieval Top-K**   | `k = 4`                                           | Balances recall vs. prompt length. Sending too many chunks increases latency and distracts the LLM; 4 chunks comfortably covers the necessary policy details.                                                    |
| **LLM Provider**      | Groq (`openai/gpt-oss-20b`)                       | Extremely low latency (free tier) and strong instruction-following capabilities for extractive QA tasks.                                                                                                         |
| **Guardrails**        | Off-topic refusal, length limit, forced citations | If the maximum cosine similarity of retrieved chunks is `< 0.25`, the system refuses to answer. Answers are capped at 150 words, and the system explicitly forces `[doc_id]` citations to prevent hallucination. |

## 3. Evaluation Approach

The system was evaluated using a custom dataset of **20 questions** (`eval/questions.jsonl`) spanning six core policy topics: PTO, Remote Work, Expenses, Security, Holidays, and Code of Conduct. Each question includes a short gold answer and the target `gold_doc_ids` that must be cited.

To run the evaluation:

```bash
python -m eval.run_eval
```
