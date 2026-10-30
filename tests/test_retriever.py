"""Smoke test — requires a populated Chroma index. Skipped if not built."""
import pytest
from src.config import CHROMA_DIR
from src.retrieval.retriever import retrieve


def _index_has_chunks() -> bool:
    """True only if a Chroma collection exists and has at least one chunk."""
    try:
        from src.ingestion.indexer import get_collection
        col = get_collection()
        return col.count() > 0
    except Exception:
        return False


@pytest.mark.skipif(not _index_has_chunks(),
                    reason="Chroma index is not built or is empty")
def test_retrieve_returns_chunks():
    hits = retrieve("How many PTO days do I get per year?", k=3)
    assert len(hits) >= 1
    assert all("doc_id" in h and "text" in h for h in hits)