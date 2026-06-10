import streamlit as st
import uuid
from datetime import datetime
from agent import run_agent

st.set_page_config(page_title="MoodBot AI", layout="wide")

st.title("🌸 MoodBot AI")

# ---------------- STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "mood_log" not in st.session_state:
    st.session_state.mood_log = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "mode" not in st.session_state:
    st.session_state.mode = "chat"

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("⚙️ Режим")

    st.session_state.mode = st.selectbox(
        "Вибір режиму",
        ["chat", "agent"]
    )

    if st.button("🧹 Очистити"):
        st.session_state.messages = []
        st.session_state.mood_log = []

    st.info(f"Thread: {st.session_state.thread_id}")

# ---------------- CHAT HISTORY ----------------
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

# ---------------- INPUT ----------------
msg = st.chat_input("Напиши щось...")

if msg:
    st.session_state.messages.append({"role": "user", "content": msg})

    # ---------------- CHAT MODE (як GPT) ----------------
    if st.session_state.mode == "chat":

        text = msg.lower()

        if "погано" in text:
            response = "💙 Мені шкода, що ти так почуваєшся. Я з тобою."
            mood_value = 1

        elif "стрес" in text:
            response = "🌿 Спробуй глибоко подихати. Я поруч."
            mood_value = 2

        elif "привіт" in text:
            response = "👋 Привіт! Як ти сьогодні?"
            mood_value = 4

        else:
            response = "💬 Розкажи більше, я тебе слухаю."
            mood_value = 3

        st.session_state.mood_log.append({
            "time": datetime.now(),
            "value": mood_value
        })

    # ---------------- AGENT MODE ----------------
    else:
        response = run_agent(msg, st.session_state.thread_id)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# ---------------- MOOD BUTTONS ----------------
st.divider()
st.subheader("😊 Обери настрій")

cols = st.columns(5)

moods = [
    ("😊", 5),
    ("🙂", 4),
    ("😐", 3),
    ("😔", 2),
    ("😢", 1)
]

for i, (emoji, value) in enumerate(moods):
    with cols[i]:
        if st.button(emoji):
            st.session_state.mood_log.append({
                "time": datetime.now(),
                "value": value
            })
            st.success("Збережено!")

# ---------------- MOOD CHART ----------------
st.divider()
st.subheader("📊 Твій настрій")

if len(st.session_state.mood_log) > 1:
    import pandas as pd

    df = pd.DataFrame(st.session_state.mood_log)
    df["date"] = pd.to_datetime(df["time"]).dt.date

    chart = df.groupby("date")["value"].mean()

    st.line_chart(chart)
else:
    st.info("Потрібно хоча б 2 записи")
