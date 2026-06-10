
import streamlit as st

st.title("🌸 MoodBot")

msg = st.chat_input("Напиши щось")

if msg:
    with st.chat_message("user"):
        st.write(msg)

    with st.chat_message("assistant"):
        st.write("Я почув тебе 💜")
