"""Prompt templates for RAG."""
from typing import List, Dict
from src.config import MAX_ANSWER_WORDS

SYSTEM_PROMPT = f"""You are a company policy assistant.
Rules:
- Answer ONLY from the provided context. Do not use outside knowledge.
- If the context does not contain the answer, reply exactly:
  "I can only answer questions about our company policies."
- Keep answers under {MAX_ANSWER_WORDS} words.
- Cite each source you use as [doc_id] at the end of the sentence that uses it.
- Never invent doc_ids; only use ones from the provided context."""


def build_user_prompt(query: str, chunks: List[Dict]) -> str:
    if not chunks:
        return f"Question: {query}\n\nContext: (empty)"
    ctx = "\n\n".join(
        f'[{c["doc_id"]}] ({c["title"]})\n{c["text"]}' for c in chunks
    )
    return f"Context:\n{ctx}\n\nQuestion: {query}\n\nAnswer (with [doc_id] citations):"