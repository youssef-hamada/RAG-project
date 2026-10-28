"""Deterministic chunking with overlap. Chunks preserve doc metadata for citations."""
from typing import List, Dict
from src.config import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    if overlap >= size:
        raise ValueError("overlap must be < size")
    chunks, i = [], 0
    while i < len(text):
        chunk = text[i:i + size].strip()
        if chunk:
            chunks.append(chunk)
        i += size - overlap
    return chunks


def chunk_documents(docs: List[Dict]) -> List[Dict]:
    out = []
    for d in docs:
        for idx, c in enumerate(chunk_text(d["text"])):
            out.append({
                "chunk_id": f'{d["doc_id"]}::{idx}',
                "doc_id": d["doc_id"],
                "title": d["title"],
                "source_path": d["source_path"],
                "text": c,
            })
    return out