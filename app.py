
import streamlit as st
from agent import run_agent

st.title("🌸 MoodBot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

msg = st.chat_input("Напиши щось")

if msg:
    st.session_state.messages.append({
        "role": "user",
        "content": msg
    })

    response = run_agent(msg)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    st.rerun()
