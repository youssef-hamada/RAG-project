"""Streamlit chat UI. Run: streamlit run src/app/streamlit_app.py"""
import streamlit as st
from src.generation.rag import answer

st.set_page_config(page_title="Company Policies RAG", page_icon="📘")
st.title("📘 Company Policies Assistant")
st.caption("Ask about PTO, remote work, expenses, security, holidays, or conduct.")

if "history" not in st.session_state:
    st.session_state.history = []

query = st.chat_input("Ask a policy question…")

if query:
    with st.spinner("Thinking…"):
        result = answer(query)
    st.session_state.history.append({"q": query, "r": result})

for turn in reversed(st.session_state.history):
    st.markdown(f"**You:** {turn['q']}")
    st.markdown(f"**Assistant:** {turn['r']['answer']}")
    if turn["r"]["sources"]:
        with st.expander("📎 Sources"):
            for s in turn["r"]["sources"]:
                st.markdown(f"**[{s['doc_id']}]** — *{s['title']}* (score={s['score']:.2f})")
                st.code(s["text"][:400] + ("…" if len(s["text"]) > 400 else ""),
                        language="text")
    st.divider()

with st.sidebar:
    st.markdown("### Status")
    try:
        from src.ingestion.indexer import get_collection
        count = get_collection().count()
        st.success(f"Index OK — {count} chunks")
    except Exception as e:
        st.error(f"Index not built: {e}")
    st.markdown("---")
    st.markdown("**Try:**")
    st.markdown("- How many PTO days do I get per year?")
    st.markdown("- What is the hotel reimbursement cap?")
    st.markdown("- Can I work from another country?")