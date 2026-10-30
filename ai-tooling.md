`design-and-evaluation.md`

````markdown
# Design & Evaluation

## 1. Architecture

data/raw/\* ──▶ loaders.py ──▶ chunker.py ──▶ indexer.py ──▶ chroma_db/
│
user query ──▶ retriever.py ──▶ prompt.py ──▶ llm.py (Groq) ──▶ guardrails.py ──▶ UI / API

Layers:

- **Ingestion** (`src/ingestion/`): `loaders.py` normalizes PDFs/MD/TXT into
  `{doc_id, title, source_path, text}` records. `chunker.py` splits into overlapping
  windows with stable `chunk_id`s. `indexer.py` embeds chunks and persists them to
  Chroma.
- **Retrieval** (`src/retrieval/retriever.py`): cosine top-k against Chroma,
  returning chunk text + metadata + similarity score.
- **Generation** (`src/generation/`): `prompt.py` injects retrieved chunks with
  `[doc_id]` tags, `llm.py` calls Groq, `rag.py` orchestrates and applies
  `guardrails.py` (off-topic refusal, word cap, citation enforcement).
- **App** (`src/app/`): Streamlit UI for humans; FastAPI for programmatic access.

## 2. Design decisions & rationale

| Choice               | Value                                                                | Why                                                                                                                                                                   |
| -------------------- | -------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Embedding model      | `sentence-transformers/all-MiniLM-L6-v2`                             | Runs locally and free; strong English short-text retrieval; no API quota risk                                                                                         |
| Vector store         | Chroma (persistent local)                                            | Zero-config, no external service, supports metadata filters for citations                                                                                             |
| Chunk size / overlap | 700 chars / 120 chars                                                | Roughly 2–3 paragraphs per chunk — enough context for policy answers without diluting retrieval with off-topic text; overlap preserves facts that straddle boundaries |
| Top-k                | 4                                                                    | Balances recall vs. prompt length and latency; empirically good for a 6-document corpus                                                                               |
| LLM                  | Groq `llama-3.1-8b-instant`                                          | Very low latency on free tier; strong instruction-following on short extractive answers                                                                               |
| Citations            | `[doc_id]` inline tokens                                             | Cheap to verify in evaluation, easy for the model to emit, directly maps to metadata stored in Chroma                                                                 |
| Refusal threshold    | cosine sim < 0.25                                                    | Off-corpus queries have low max similarity to any policy chunk; refusing earlier beats hallucinating                                                                  |
| Output cap           | 150 words                                                            | Keeps answers extractive and grounded; reduces citation drift                                                                                                         |
| Determinism          | No sampling; `temperature=0.1`; fixed `SEED=42`; char-based chunking | Makes eval reproducible across runs                                                                                                                                   |

## 3. Evaluation approach

- **Dataset:** 20 questions in `eval/questions.jsonl` across five topics (PTO,
  remote work, expenses, security, holidays, conduct). Each has a short gold
  answer and the doc_id(s) that should be cited.
- **Groundedness (required):** LLM-as-judge — a separate cheap LLM call is asked
  whether every factual claim in the answer is supported by the retrieved context.
  Binary yes/no, aggregated to a percentage.
- **Citation accuracy (required):** Each answer's `[doc_id]` citations are extracted
  and checked to be a subset of the gold doc_ids. Answers with no citations are
  counted as inaccurate.
- **Partial match (optional):** `gold_answer` normalized-substring check.
- **Latency (required):** Wall-clock ms per question measured around `rag.answer()`;
  p50 and p95 reported from the sorted latencies.
- **Ablations (optional):** Not run in this iteration; natural next steps are
  sweeping `TOP_K ∈ {2,4,6}` and `CHUNK_SIZE ∈ {500,700,900}` and comparing
  groundedness/citation accuracy.

Run:

````bash
python -m scripts.build_index
python -m eval.run_eval


`ai-tooling.md`
```markdown
# AI Tooling

This project was built with heavy AI assistance as encouraged by the brief. This
file documents which tools were used, for what, and how well they worked.

## Tools used

### ChatGPT / Claude (chat)
- **Used for:** scaffolding the file layout, drafting the RAG orchestration code,
  writing the evaluation harness, drafting `README.md` and this file.
- **Worked well:** Near-instant drafts for the ingestion → chunker → indexer
  pipeline; fast iteration on prompt wording; useful sanity-check on
  guardrail thresholds.
- **Didn't work:** Defaulted to OpenAI models in early drafts and needed
  correction to use Groq; sometimes produced eval metrics code that assumed
  the answer contained a `[doc_id]` citation — required manual guardrail to
  enforce that invariant in `guardrails.py`.

### Cursor (AI IDE)
- **Used for:** small refactors (renaming, moving helpers), inline edits to
  `src/app/api.py` while iterating on the Pydantic response model.
- **Worked well:** Fast at mechanical edits across multiple files.
- **Didn't work:** Occasionally suggested installing packages not in
  `requirements.txt`; had to pin versions manually.

### GitHub Copilot Chat (in VS Code)
- **Used for:** docstring completion in `src/ingestion/*` and `src/retrieval/*`;
  asking "why is this import failing" while wiring the FastAPI `TestClient`.
- **Worked well:** Excellent at short, well-scoped Python questions.
- **Didn't work:** No project-level context, so it couldn't reason about the
  ingestion→retrieval coupling; still needed me to specify the contract
  (`chunks` list shape) in each prompt.

## Human work

- All design decisions (chunk size, top_k, thresholds, metric definitions)
- Writing the 20-question gold eval set by hand from the corpus so evaluation
  is meaningful and not model-generated
- Verifying citation accuracy by spot-checking answers against documents
- Manual QA on the Streamlit UI and guardrail refusal behavior

## Non-AI dependencies

- `sentence-transformers`, `chromadb`, `groq`, `streamlit`, `fastapi`,
  `pypdf`, `pytest` — installed from `requirements.txt`.
````
````
