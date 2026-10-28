"""Groq LLM client. Returns plain text."""
from groq import Groq
from src.config import GROQ_API_KEY, LLM_MODEL


def llm_chat(system: str, user: str, temperature: float = 0.1) -> str:
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is not set. See .env.example.")
    client = Groq(api_key=GROQ_API_KEY)
    resp = client.chat.completions.create(
        model=LLM_MODEL,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return resp.choices[0].message.content.strip()