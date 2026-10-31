"""Run the eval set. Writes eval/results.json."""
import json, re, time, statistics
from pathlib import Path
from src.generation.rag import answer
from src.generation.llm import llm_chat

EVAL_DIR = Path(__file__).parent
QUESTIONS = EVAL_DIR / "questions.jsonl"
OUT = EVAL_DIR / "results.json"

JUDGE_SYSTEM = """You are a strict grader. Given a question, an answer, and the retrieved context, decide if EVERY factual claim in the answer is supported by the context. Reply with exactly YES or NO."""

def _normalize_id(s: str) -> str:
    # Makes "pto-policy", "pto_policy", and "PTO_POLICY" all match
    return s.lower().replace("-", "_").strip()

def _is_grounded(question: str, ans: str, sources: list) -> bool:
    if not sources:
        return ans.strip().lower().startswith("i can only answer")
    ctx = "\n\n".join(s["text"] for s in sources)
    try:
        verdict = llm_chat(
            JUDGE_SYSTEM,
            f"Question: {question}\nAnswer: {ans}\nContext:\n{ctx}",
            temperature=0.0,
        ).strip().upper()
        return verdict.startswith("YES")
    except Exception as e:
        print(f"  [Judge Error] {e}")
        # fallback
        ans_words = set(re.findall(r'\w+', ans.lower()))
        ctx_words = set(re.findall(r'\w+', ctx.lower()))
        if not ans_words:
            return False
        overlap = len(ans_words & ctx_words) / len(ans_words)
        return overlap >= 0.5

def _citation_correct(ans: str, gold_ids: list, sources: list) -> bool:
    # Extract citations like [pto-policy] or [pto_policy]
    cited = set(re.findall(r"\[([a-zA-Z0-9_\-]+)\]", ans))
    cited = {_normalize_id(c) for c in cited}
    gold = {_normalize_id(g) for g in gold_ids}
    
    if not cited:
        return False
    # Every citation must be in the gold list
    return cited.issubset(gold)

def _partial_match(ans: str, gold: str) -> bool:
    return _normalize_id(gold) in _normalize_id(ans)

def main():
    rows = [json.loads(l) for l in QUESTIONS.read_text().splitlines() if l.strip()]
    results, latencies = [], []
    
    print(f"Running {len(rows)} questions...\n")
    
    for row in rows:
        t0 = time.perf_counter()
        try:
            r = answer(row["question"])
        except Exception as e:
            r = {"answer": f"ERROR: {e}", "sources": []}
        latency_ms = (time.perf_counter() - t0) * 1000
        latencies.append(latency_ms)

        sources = r["sources"]
        grounded = _is_grounded(row["question"], r["answer"], sources)
        cited_ok = _citation_correct(r["answer"], row["gold_doc_ids"], sources)
        partial = _partial_match(r["answer"], row["gold_answer"])

        results.append({
            "id": row["id"], "topic": row["topic"],
            "question": row["question"],
            "answer": r["answer"],
            "cited_doc_ids": sorted(set(re.findall(r"\[([a-zA-Z0-9_\-]+)\]", r["answer"]))),
            "gold_doc_ids": row["gold_doc_ids"],
            "grounded": grounded,
            "citation_correct": cited_ok,
            "partial_match": partial,
            "latency_ms": round(latency_ms, 1),
        })
        print(f'{row["id"]:>4}  grounded={grounded!s:5} cite={cited_ok!s:5} partial={partial!s:5}  {latency_ms:7.0f} ms')

    n = len(results)
    latencies.sort()
    def pct(p): return latencies[int(round((p/100)*(n-1)))]
    
    summary = {
        "n": n,
        "groundedness_pct": round(100 * sum(r["grounded"] for r in results) / n, 1),
        "citation_accuracy_pct": round(100 * sum(r["citation_correct"] for r in results) / n, 1),
        "partial_match_pct": round(100 * sum(r["partial_match"] for r in results) / n, 1),
        "latency_p50_ms": round(pct(50), 1),
        "latency_p95_ms": round(pct(95), 1),
        "latency_mean_ms": round(statistics.mean(latencies), 1),
    }
    
    OUT.write_text(json.dumps({"summary": summary, "results": results}, indent=2))
    print("\n=== SUMMARY ===")
    print(json.dumps(summary, indent=2))
    print(f"\nWrote {OUT}")

if __name__ == "__main__":
    main()