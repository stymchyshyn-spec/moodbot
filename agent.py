
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

    # 1. Запис настрою
    if "настрій" in msg or "поганий" in msg or "хороший" in msg:
        return "💜 Я зрозумів твій настрій і записав його. Якщо хочеш, можеш розказати більше."

    # 2. Запит по аналізу
    if "аналіз" in msg or "що зі мною" in msg:
        return "📊 Ти зараз у процесі проживання емоцій. Це нормально. Я поруч 💙"

    # 3. Поради
    if "що робити" in msg or "покращити" in msg:
        return (
            "🌿 Ось що може допомогти:\n"
            "- прогулянка\n"
            "- вода / чай\n"
            "- відпочинок без телефону\n"
            "- написати свої думки\n"
        )

    # 4. Загальні фрази (НЕ повторюєм “я тебе почув”)
    if "привіт" in msg:
        return "👋 Привіт! Як ти себе почуваєш сьогодні?"

    if "розказати" in msg:
        return "💬 Розкажи мені, що саме тебе турбує або радує"

    # 5. fallback (ВАЖЛИВО — НЕ повторюємо текст)
    return "💙 Я тебе слухаю. Можеш розповісти детальніше?"
