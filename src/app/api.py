"""FastAPI service. Run: uvicorn src.app.api:app --reload"""
from fastapi import FastAPI
from pydantic import BaseModel, Field
from src.generation.rag import answer
from src.ingestion.indexer import get_collection

app = FastAPI(title="Company Policies RAG API")


class ChatIn(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000)


class Citation(BaseModel):
    doc_id: str
    title: str
    snippet: str


class ChatOut(BaseModel):
    answer: str
    citations: list[Citation]


@app.get("/health")
def health():
    try:
        n = get_collection().count()
        return {"status": "ok", "indexed_chunks": n}
    except Exception as e:
        return {"status": "degraded", "error": str(e)}


@app.post("/chat", response_model=ChatOut)
def chat(body: ChatIn):
    r = answer(body.question)
    return {
        "answer": r["answer"],
        "citations": [
            {
                "doc_id": c["doc_id"],
                "title": c["title"],
                "snippet": c["text"][:300] + ("…" if len(c["text"]) > 300 else ""),
            }
            for c in r["sources"]
        ],
    }