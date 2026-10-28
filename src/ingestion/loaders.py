"""Load PDFs, Markdown, and TXT files from data/raw into normalized documents."""
from pathlib import Path
from typing import List, Dict
from pypdf import PdfReader


def load_pdf(path: Path) -> str:
    reader = PdfReader(str(path))
    return "\n".join((page.extract_text() or "") for page in reader.pages)


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _title_from_stem(stem: str) -> str:
    return stem.replace("_", " ").replace("-", " ").title()


def load_all(data_dir: str) -> List[Dict]:
    """Return list of {doc_id, title, source_path, text}."""
    docs = []
    for p in sorted(Path(data_dir).rglob("*")):
        suffix = p.suffix.lower()
        if suffix == ".pdf":
            text = load_pdf(p)
        elif suffix in (".md", ".txt"):
            text = load_text(p)
        else:
            continue
        if not text.strip():
            continue
        docs.append({
            "doc_id": p.stem,
            "title": _title_from_stem(p.stem),
            "source_path": str(p),
            "text": text,
        })
    return docs