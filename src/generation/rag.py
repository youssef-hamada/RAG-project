"""End-to-end RAG: retrieve -> generate -> guardrails."""
from typing import Dict
from src.config import TOP_K
from src.retrieval.retriever import retrieve
from src.generation.llm import llm_chat
from src.generation.prompt import SYSTEM_PROMPT, build_user_prompt
from src.generation.guardrails import (
    is_off_topic, enforce_max_words, ensure_citation, REFUSAL,
)


def answer(query: str, k: int = TOP_K) -> Dict:
    chunks = retrieve(query, k=k)
    if not chunks or is_off_topic(chunks):
        return {"answer": REFUSAL, "sources": []}

    raw = llm_chat(SYSTEM_PROMPT, build_user_prompt(query, chunks))
    raw = enforce_max_words(raw)
    raw = ensure_citation(raw, chunks)
    return {"answer": raw, "sources": chunks}