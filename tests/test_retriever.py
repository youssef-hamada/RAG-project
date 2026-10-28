"""Smoke test — requires chroma index to exist. Skipped if not built."""
import os
import pytest
from src.config import CHROMA_DIR
from src.retrieval.retriever import retrieve


@pytest.mark.skipif(not os.path.isdir(CHROMA_DIR) or not os.listdir(CHROMA_DIR),
                    reason="index not built")
def test_retrieve_returns_chunks():
    hits = retrieve("How many PTO days do I get per year?", k=3)
    assert len(hits) >= 1
    assert all("doc_id" in h and "text" in h for h in hits)