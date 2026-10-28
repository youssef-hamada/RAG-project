"""End-to-end index build. Run: python -m scripts.build_index"""
from src.config import DATA_DIR
from src.ingestion.loaders import load_all
from src.ingestion.chunker import chunk_documents
from src.ingestion.indexer import build_index


def main():
    docs = load_all(str(DATA_DIR))
    chunks = chunk_documents(docs)
    print(f"Loaded {len(docs)} docs, produced {len(chunks)} chunks.")
    build_index(chunks, reset=True)
    print("Index built at chroma_db/")


if __name__ == "__main__":
    main()