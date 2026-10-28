"""Top-k cosine retrieval against Chroma."""
from typing import List, Dict
from sentence_transformers import SentenceTransformer
from src.config import EMBED_MODEL, TOP_K
from src.ingestion.indexer import get_collection

_model = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBED_MODEL)
    return _model


def retrieve(query: str, k: int = TOP_K) -> List[Dict]:
    col = get_collection()
    q_emb = _get_model().encode([query], normalize_embeddings=True).tolist()
    res = col.query(
        query_embeddings=q_emb, n_results=k,
        include=["documents", "metadatas", "distances"],
    )
    out = []
    if not res.get("documents") or not res["documents"][0]:
        return out
    for text, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
        out.append({
            "text": text,
            "doc_id": meta["doc_id"],
            "title": meta["title"],
            "source_path": meta.get("source_path", ""),
            "score": 1.0 - float(dist),
        })
    return out