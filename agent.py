def run_agent(user_message: str, thread_id: str = "", context=None, strict=False):

    msg = user_message.lower()

    # ---------------- STRICT MODE (agent) ----------------
    if strict:
        if "настрій" in msg:
            return "💜 Я зафіксував твій стан."

        if "що робити" in msg:
            return "🌿 Спробуй відпочинок, воду, прогулянку."

        if "аналіз" in msg:
            return "📊 Я бачу твої емоції через повідомлення."

        return "🤖 Agent mode: виконую запит"

    # ---------------- CHAT MODE (майже GPT) ----------------

    # реакція на контекст
    last_user_msgs = [m["content"] for m in context if m["role"] == "user"] if context else []

    if any("погано" in m.lower() for m in last_user_msgs):
        return "💙 Схоже, тобі зараз непросто. Хочеш поговоримо про це?"

    if any("стрес" in m.lower() for m in last_user_msgs):
        return "🌿 Я поруч. Давай знайдемо, що тебе заспокоїть."

    if "привіт" in msg:
        return "👋 Привіт! Як ти себе сьогодні почуваєш?"

    if "як справи" in msg:
        return "💬 У мене все стабільно 🙂 А як ти?"

    if "що ти можеш" in msg:
        return "🤖 Я можу підтримати тебе, поговорити і допомогти з настроєм."

    # fallback як GPT
    return "💭 Розкажи трохи більше, я тебе слухаю."
