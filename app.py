
import streamlit as st
import uuid
from agent import run_agent

st.set_page_config(page_title="MoodGPT", layout="wide")

st.title("🌸 MoodGPT (майже як GPT)")

# ---------------- STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "mode" not in st.session_state:
    st.session_state.mode = "chat"

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("⚙️ Режим")

    st.session_state.mode = st.radio(
        "Вибір режиму",
        ["chat", "agent"]
    )

    if st.button("🧹 Очистити"):
        st.session_state.messages = []

    st.info("MoodGPT працює без API, але з логікою як у GPT")

# ---------------- CHAT HISTORY ----------------
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

# ---------------- INPUT ----------------
msg = st.chat_input("Напиши щось...")

if msg:
    st.session_state.messages.append({"role": "user", "content": msg})

    # CONTEXT (останні 6 повідомлень)
    context = st.session_state.messages[-6:]

    if st.session_state.mode == "chat":
        response = run_agent(msg, st.session_state.thread_id, context)
    else:
        response = run_agent(msg, st.session_state.thread_id, context, strict=True)

    st.session_state.messages.append({"role": "assistant", "content": response})

    st.rerun()
