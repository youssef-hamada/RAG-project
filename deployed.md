# Deployment

## FastAPI service (Render free tier)

- URL: https://policies-rag-api.onrender.com
- Health: https://policies-rag-api.onrender.com/health
- Chat: POST https://policies-rag-api.onrender.com/chat
  Body: `{"question": "How many PTO days do I get per year?"}`

## Streamlit UI (Streamlit Community Cloud)

- URL: https://<your-app>.streamlit.app
- Entry point: `src/app/streamlit_app.py`
- Secrets: `GROQ_API_KEY` set in Streamlit Cloud → App → Settings → Secrets

## How to reproduce deployment

1. Fork/clone the repo to your own GitHub account.
2. **Render:** create a new Blueprint from `render.yaml`. Set `GROQ_API_KEY` in
   the Render dashboard. Add the deploy hook URL as the `RENDER_DEPLOY_HOOK`
   secret in your GitHub repo (Settings → Secrets → Actions).
3. **Streamlit Cloud:** create a new app pointing at this repo, entry point
   `src/app/streamlit_app.py`, and paste `GROQ_API_KEY=...` into Secrets.

If the deployed service is cold (free tier), the first `/chat` request may take
~30 seconds while the instance boots and the index builds.
