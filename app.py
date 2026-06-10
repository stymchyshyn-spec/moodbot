pip install streamlit langgraph langchain langchain-google-genai langchain-community python-dotenv google-genai
!pip install -q langchain-mistralai
from langchain_mistralai.chat_models import ChatMistralAI

llm = ChatMistralAI(
    api_key="xzlx0f7OB4hMiCol0IDNconlKuOkuy8B",
    model="mistral-large-latest"
)
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import uuid
st.set_page_config(page_title="MoodBot", layout="wide")
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
}
.mood-card {
    background: white;
    padding: 1rem;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)
if "mood_log" not in st.session_state:
    st.session_state.mood_log = []

if "selected_mood" not in st.session_state:
    st.session_state.selected_mood = None

if "show_note_input" not in st.session_state:
    st.session_state.show_note_input = False
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Привіт! Я MoodBot. Скажи, як ти сьогодні почуваєшся?"
        }
    ]

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "settings" not in st.session_state:
    st.session_state.settings = {
        "mode": "chat",
        "temperature": 0.7,
        "max_tokens": 500
    }
st.sidebar.title("Налаштування MoodBot")

mode = st.sidebar.selectbox(
    "Режим роботи",
    ["chat", "agent"]
)
st.session_state.settings["mode"] = mode

temperature = st.sidebar.slider(
    "Температура",
    0.0, 1.0, 0.7, 0.1
)
st.session_state.settings["temperature"] = temperature

max_tokens = st.sidebar.slider(
    "Max tokens",
    100, 2000, 500, 100
)
st.session_state.settings["max_tokens"] = max_tokens

if st.sidebar.button("Очистити історію"):
    st.session_state.messages = []
    st.session_state.mood_log = []
    st.session_state.thread_id = str(uuid.uuid4())
    st.sidebar.success("Очищено!")


st.sidebar.info(
    f"""
  MoodBot

Режим: {st.session_state.settings['mode']}
Thread: {st.session_state.thread_id}
"""
)
st.title("🌸 Щоденник настрою")
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Напиши, як ти себе почуваєш.")
if user_input:

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    if mode == "chat":
        assistant_response = f"💬 Chat: {user_input}"
    else:
        assistant_response = run_agent(
            user_input,
            st.session_state.thread_id
        )

    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_response}
    )

    st.rerun()

mood_cols = st.columns(5)

moods = [
    ("😊", "Радість", 5),
    ("😌", "Спокій", 4),
    ("😐", "Нейтрально", 3),
    ("😔", "Сум", 2),
    ("😰", "Тривога", 1)
]

for i, (emoji, name, value) in enumerate(moods):
    with mood_cols[i]:
        if st.button(emoji, key=f"mood_{i}"):
            st.session_state.selected_mood = {
                "emoji": emoji,
                "name": name,
                "value": value
            }
            st.session_state.show_note_input = True
if st.session_state.show_note_input:
    note = st.text_area(
        f"Додай думки до настрою {st.session_state.selected_mood['emoji']}"
    )

    if st.button("💾 Зберегти"):
        st.session_state.mood_log.append({
            "timestamp": str(datetime.now()),
            "mood": st.session_state.selected_mood["name"],
            "value": st.session_state.selected_mood["value"],
            "note": note
        })

        st.session_state.show_note_input = False
        st.success("Збережено 💜")
        st.rerun()
st.divider()
st.subheader("📊 Графік настрою")

if len(st.session_state.mood_log) >= 2:
    import pandas as pd

    df = pd.DataFrame(st.session_state.mood_log)
    df["date"] = pd.to_datetime(df["timestamp"]).dt.date
    chart_data = df.groupby("date")["value"].mean()

    st.line_chart(chart_data)
else:
    st.info("Потрібно мінімум 2 записи")
@st.cache_resource
def get_llm():
    return ChatMistralAI(
        model="mistral-large-latest",
        api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=st.session_state.settings["temperature"]
    )
def build_chat_history():
    history = []

    for msg in st.session_state.messages:
        history.append(
            {
                "role": msg["role"],
                "content": msg["content"]
            }
        )

    return history
def stream_response(user_message):
    llm = get_llm()

    response = llm.stream(user_message)

    for chunk in response:
        if chunk.content:
            yield chunk.content
def run_agent(user_message):

    thread_id = st.session_state.thread_id

    response = (
        f"Agent mode\n"
        f"Thread ID: {thread_id}\n\n"
        f"Повідомлення: {user_message}"
    )

    return response
