"""Central configuration. Import constants from here."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Get the absolute path to the project root
ROOT = Path(__file__).resolve().parent.parent

# Force dotenv to load exactly this file
load_dotenv(ROOT / ".env")

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "raw"
CHROMA_DIR = ROOT / "chroma_db"
COLLECTION_NAME = "policies"

CHUNK_SIZE = 700
CHUNK_OVERLAP = 120
TOP_K = 4
MAX_ANSWER_WORDS = 150
MIN_SIMILARITY = 0.25

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "openai/gpt-oss-20b"

SEED = 42
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")