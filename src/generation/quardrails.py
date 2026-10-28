"""Guardrails: off-topic refusal, max length, citation enforcement."""
from typing import List, Dict
from src.config import MAX_ANSWER_WORDS, MIN_SIMILARITY

REFUSAL = "I can only answer questions about our company policies."


def is_off_topic(chunks: List[Dict]) -> bool:
    """True if no chunk clears the minimum similarity threshold."""
    if not chunks:
        return True
    return max(c.get("score", 0.0) for c in chunks) < MIN_SIMILARITY


def enforce_max_words(text: str, limit: int = MAX_ANSWER_WORDS) -> str:
    words = text.split()
    if len(words) <= limit:
        return text
    return " ".join(words[:limit]).rstrip(",;: ") + "…"


def ensure_citation(answer: str, chunks: List[Dict]) -> str:
    """If the answer has no [doc_id] citation for any retrieved chunk, append the top one."""
    if not chunks:
        return answer
    if any(f'[{c["doc_id"]}]' in answer for c in chunks):
        return answer
    return f'{answer.rstrip()} [{chunks[0]["doc_id"]}]'