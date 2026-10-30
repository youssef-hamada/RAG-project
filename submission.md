# Submission

## Links

- **GitHub repository:** <paste-your-repo-url>
- **Demo video (5–10 min):** <paste-your-video-url>

## Repo is shared with

- GitHub account: `quantic-grader` (repo Settings → Collaborators)

## Checklist

- [x] `README.md` — setup + run instructions
- [x] `design-and-evaluation.md` — architecture, decisions, eval results
- [x] `ai-tooling.md` — AI tools used and how
- [x] `requirements.txt` — pinned dependencies
- [x] `.env.example` — required environment variables
- [x] `data/raw/` — policy corpus
- [x] `chroma_db/` built via `python -m scripts.build_index`
- [x] `eval/questions.jsonl` (20 questions) and `eval/results.json`
- [x] `.github/workflows/ci.yml` — CI on push/PR
- [x] (optional) `.github/workflows/deploy.yml` + `render.yaml` + `deployed.md`
- [x] (optional) `docs/screenshots/` populated
- [x] Demo video recorded, all group members on camera with government ID

## Submission steps

1. Verify CI is green on `main`.
2. Open a PR → confirm CI runs → merge.
3. Ensure `quantic-grader` has read access to the repo.
4. Create a single PDF containing the two links above.
5. Upload the PDF via the dashboard **Submit Project** button (one submitter per group).
