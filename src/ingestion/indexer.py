"""Build a persistent Chroma index of chunk embeddings."""
import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict
from src.config import CHROMA_DIR, COLLECTION_NAME, EMBED_MODEL

_model = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBED_MODEL)
    return _model


def build_index(chunks: List[Dict], reset: bool = False):
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    if reset:
        try:
            client.delete_collection(COLLECTION_NAME)
        except Exception:
            pass
    col = client.get_or_create_collection(
        COLLECTION_NAME, metadata={"hnsw:space": "cosine"}
    )
    if not chunks:
        return col
    model = _get_model()
    texts = [c["text"] for c in chunks]
    embs = model.encode(texts, show_progress_bar=True, normalize_embeddings=True).tolist()
    col.add(
        ids=[c["chunk_id"] for c in chunks],
        embeddings=embs,
        documents=texts,
        metadatas=[
            {"doc_id": c["doc_id"], "title": c["title"], "source_path": c["source_path"]}
            for c in chunks
        ],
    )
    return col


def get_collection():
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_or_create_collection(COLLECTION_NAME)