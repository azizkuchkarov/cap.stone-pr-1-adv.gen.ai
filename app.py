import os
import streamlit as st

from rag.config import settings
from rag.vectorstore import FAISSStore
from rag.prompts import SYSTEM_PROMPT, ANSWER_PROMPT
from rag.tools import CREATE_TICKET_TOOL
from rag.llm import run_chat_with_tools
from rag.utils import format_context, is_answerable

st.set_page_config(page_title="RAG Support Chat", page_icon="💬", layout="wide")

@st.cache_resource
def load_store():
    store = FAISSStore(settings.EMBED_MODEL)
    if os.path.exists(settings.FAISS_INDEX_PATH) and os.path.exists(settings.DOCSTORE_PATH):
        store.load(settings.FAISS_INDEX_PATH, settings.DOCSTORE_PATH)
        return store
    return None

store = load_store()

st.title("💬 Customer Support RAG (Capstone)")
st.caption(f"Company: {settings.COMPANY_NAME} | {settings.COMPANY_EMAIL} | {settings.COMPANY_PHONE}")

with st.sidebar:
    st.header("Ticket info")
    user_name = st.text_input("Your name", value=st.session_state.get("user_name", ""))
    user_email = st.text_input("Your email", value=st.session_state.get("user_email", ""))
    st.session_state["user_name"] = user_name
    st.session_state["user_email"] = user_email

    st.divider()
    st.header("RAG settings")
    top_k = st.slider("Top K", 1, 10, settings.TOP_K)
    min_score = st.slider("Min similarity threshold", 0.0, 1.0, settings.MIN_SIM_SCORE)

    st.divider()
    st.header("Index status")
    if store is None:
        st.error("Vector index not found. Run `python ingest.py` locally and commit `data/processed/*`.")
    else:
        st.success("Index loaded.")

if "chat" not in st.session_state:
    st.session_state["chat"] = []  # list of {role, content}

def render_chat():
    for m in st.session_state["chat"]:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

render_chat()

user_q = st.chat_input("Ask a question about the documents, or ask to create a ticket...")

if user_q:
    st.session_state["chat"].append({"role": "user", "content": user_q})
    with st.chat_message("user"):
        st.markdown(user_q)

    if store is None:
        answer = "Index not available. Please run `python ingest.py` and commit the processed files."
        st.session_state["chat"].append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.markdown(answer)
        st.stop()

    # Retrieve
    snips = store.search(user_q, top_k=top_k)

    # Build context text for LLM
    context = format_context(snips)
    history_text = "\n".join([f'{m["role"]}: {m["content"]}' for m in st.session_state["chat"][-12:]])

    # Decide whether answerable
    if not is_answerable(snips, min_score=min_score):
        # Encourage ticket creation
        suggest = (
            "I couldn’t find a confident answer in the provided documents.\n\n"
            "If you want, I can create a support ticket. Please reply with:\n"
            "- **create ticket** and include any extra details you want.\n\n"
            f"You can also contact {settings.COMPANY_NAME} directly at {settings.COMPANY_EMAIL}."
        )
        st.session_state["chat"].append({"role": "assistant", "content": suggest})
        with st.chat_message("assistant"):
            st.markdown(suggest)
        st.stop()

    # Use function calling tools ALWAYS available (must-have requirement)
    prompt = ANSWER_PROMPT.format(history=history_text, context=context, question=user_q)

    messages = [
        {"role": "user", "content": prompt}
    ]

    # If user explicitly requests ticket, nudge tool call by adding instruction
    wants_ticket = ("create ticket" in user_q.lower()) or ("open ticket" in user_q.lower()) or ("raise ticket" in user_q.lower())

    if wants_ticket:
        if not user_name or not user_email:
            reply = "Please fill your name and email in the sidebar so I can create the ticket."
            st.session_state["chat"].append({"role": "assistant", "content": reply})
            with st.chat_message("assistant"):
                st.markdown(reply)
            st.stop()

        # Add an instruction that encourages tool call
        messages = [
            {"role": "user", "content": prompt + f"\n\nUser wants a ticket. Use the tool to create it.\nUser name: {user_name}\nUser email: {user_email}"}
        ]

    out = run_chat_with_tools(
        system_prompt=SYSTEM_PROMPT,
        messages=messages,
        tools=[CREATE_TICKET_TOOL],
    )

    answer = out["final_text"]
    st.session_state["chat"].append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)

    # Optional: show retrieved context in an expander (useful for grading)
    with st.expander("Retrieved context (for debugging / grading)"):
        st.text(context)
