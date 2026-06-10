
from datetime import datetime

# -------------------
# SIMPLE MEMORY
# -------------------
mood_log = []


# -------------------
# TOOLS (без LangGraph/LLM для стабільності)
# -------------------
def add_mood(mood: str, note: str) -> str:
    mood_log.append({
        "timestamp": datetime.now().isoformat(),
        "mood": mood,
        "note": note
    })
    return f"Настрій '{mood}' збережено."


def last_moods(n: int = 5) -> str:
    return str(mood_log[-n:]) if mood_log else "Порожньо"


def mood_summary(n: int = 7) -> str:
    return f"Записів: {len(mood_log)}"


def current_datetime(query: str = "") -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# -------------------
# SIMPLE AGENT FUNCTION
# -------------------
def run_agent(user_message: str, thread_id: str = ""):

    msg = user_message.lower()

    if "запис" in msg or "настрій" in msg:
        return add_mood("neutral", user_message)

    if "останні" in msg:
        return last_moods()

    if "аналіз" in msg:
        return mood_summary()

    if "дата" in msg:
        return current_datetime()

    return f"Agent mode: я отримав повідомлення → {user_message}"
def run_agent(user_message: str, thread_id: str = ""):

    msg = user_message.lower()

    if "настрій" in msg or "почуваю" in msg:
        return add_mood("neutral", user_message)

    if "останні" in msg:
        return last_moods()

    if "аналіз" in msg:
        return mood_summary()

    if "дата" in msg:
        return current_datetime()

    return f"💬 Я почув тебе: {user_message}"
