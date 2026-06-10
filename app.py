
import streamlit as st
from agent import run_agent

st.set_page_config(page_title="MoodBot", layout="wide")

st.title("🌸 MoodBot")

# -------------------------
# SESSION STATE
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "mood_history" not in st.session_state:
    st.session_state.mood_history = []

if "mode" not in st.session_state:
    st.session_state.mode = "chat"

# -------------------------
# SIDEBAR
# -------------------------
with st.sidebar:
    st.header("⚙️ Налаштування")

    mode = st.radio("Режим", ["chat", "agent"])
    st.session_state.mode = mode

    if st.button("🧹 Очистити чат"):
        st.session_state.messages = []
        st.session_state.mood_history = []

    st.info("MoodBot — простий AI для настрою")

# -------------------------
# CHAT HISTORY
# -------------------------
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

# -------------------------
# INPUT
# -------------------------
msg = st.chat_input("Напиши щось...")

if msg:
    st.session_state.messages.append({"role": "user", "content": msg})

    # -------- MODE LOGIC --------
    if st.session_state.mode == "chat":
        if "поган" in msg.lower():
            response = "💜 Мені шкода, що тобі так. Я поруч."
            st.session_state.mood_history.append(1)

        elif "норм" in msg.lower():
            response = "🙂 Зрозуміло, тримаєш баланс"
            st.session_state.mood_history.append(3)

        else:
            response = "💬 Я тебе слухаю"
            st.session_state.mood_history.append(4)

    else:
        response = run_agent(msg)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# -------------------------
# MOOD GRAPH
# -------------------------
st.divider()
st.subheader("📊 Графік настрою")

if st.session_state.mood_history:
    st.line_chart(st.session_state.mood_history)
else:
    st.write("Поки немає даних")
