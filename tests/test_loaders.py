from src.ingestion.loaders import load_all
from src.config import DATA_DIR


def test_load_all_finds_docs():
    docs = load_all(DATA_DIR)
    assert len(docs) >= 6
    for d in docs:
        assert d["text"].strip()
        assert d["doc_id"]
        assert d["title"]