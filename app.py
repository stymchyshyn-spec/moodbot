
import streamlit as st
import json
import uuid
from agent import run_agent

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="MoodBot AI",
    page_icon="🌸",
    layout="wide"
)

# ---------------------------
# CSS (UI кастомізація)
# ---------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f5f7fa, #e4e8ec);
}
.chat-box {
    padding: 10px;
    border-radius: 10px;
    background: white;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# SESSION STATE
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "settings" not in st.session_state:
    st.session_state.settings = {
        "mode": "chat",
        "temperature": 0.7,
        "max_tokens": 500,
        "system_prompt": "Ти дружній MoodBot"
    }

# ---------------------------
# SIDEBAR
# ---------------------------
with st.sidebar:
    st.title("⚙️ Налаштування")

    st.session_state.settings["mode"] = st.selectbox(
        "Режим",
        ["chat", "agent"]
    )

    st.session_state.settings["temperature"] = st.slider(
        "Температура",
        0.0, 1.0, 0.7
    )

    st.session_state.settings["max_tokens"] = st.slider(
        "Max tokens",
        100, 2000, 500
    )

    st.session_state.settings["system_prompt"] = st.text_area(
        "System prompt",
        st.session_state.settings["system_prompt"]
    )

    if st.button("🧹 Очистити історію"):
        st.session_state.messages = []

    st.info(f"""
    MoodBot AI  
    Thread: {st.session_state.thread_id}  
    Messages: {len(st.session_state.messages)}
    """)

# ---------------------------
# HEADER
# ---------------------------
st.title("🌸 MoodBot AI")

# ---------------------------
# CHAT HISTORY
# ---------------------------
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

# ---------------------------
# INPUT
# ---------------------------
user_input = st.chat_input("Напиши щось...")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # MODE SWITCH
    if st.session_state.settings["mode"] == "chat":
        response = f"💬 {user_input}"
    else:
        response = run_agent(user_input, st.session_state.thread_id)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    st.rerun()

# ---------------------------
# UI COMPONENTS (REQUIREMENT 6)
# ---------------------------
tab1, tab2 = st.tabs(["📊 Статистика", "📥 Експорт"])

with tab1:
    st.subheader("Метрики")

    st.metric("Повідомлення", len(st.session_state.messages))

    approx_tokens = len(" ".join([m["content"] for m in st.session_state.messages])) // 4
    st.metric("≈ Токени", approx_tokens)

with tab2:
    st.subheader("Експорт чату")

    st.download_button(
        "⬇️ Download JSON",
        data=json.dumps(st.session_state.messages, ensure_ascii=False, indent=2),
        file_name="chat.json"
    )
