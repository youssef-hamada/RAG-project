from src.ingestion.chunker import chunk_text, chunk_documents


def test_chunk_text_respects_size_and_overlap():
    text = "a" * 2000
    chunks = chunk_text(text, size=700, overlap=120)
    assert all(len(c) <= 700 for c in chunks)
    assert len(chunks) >= 3


def test_chunk_documents_has_metadata():
    docs = [{"doc_id": "x", "title": "X", "source_path": "x.md", "text": "hello world " * 100}]
    chunks = chunk_documents(docs)
    assert chunks[0]["chunk_id"].startswith("x::")
    assert chunks[0]["doc_id"] == "x"