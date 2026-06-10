
import streamlit as st
from agent import run_agent

st.set_page_config(page_title="MoodBot", layout="wide")

st.title("🌸 MoodBot")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "mode" not in st.session_state:
    st.session_state.mode = "chat"

# показ історії
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

msg = st.chat_input("Напиши щось")

if msg:
    st.session_state.messages.append({"role": "user", "content": msg})

    if st.session_state.mode == "chat":
        response = f"💬 Chat: {msg}"
    else:
        response = run_agent(msg)

    st.session_state.messages.append({"role": "assistant", "content": response})

    st.rerun()
