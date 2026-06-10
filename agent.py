
def run_agent(user_message: str, thread_id: str = ""):

    msg = user_message.lower()

    if "настрій" in msg:
        return "💜 Я зрозумів твій настрій і зберіг його"

    if "погано" in msg:
        return "🌿 Мені шкода. Спробуй відпочити або прогулянку"

    if "що робити" in msg:
        return "✨ Прогулянка, вода, відпочинок — це допоможе"

    if "привіт" in msg:
        return "👋 Привіт! Як ти себе почуваєш?"

    if "останні" in msg:
        return "📊 Я можу показати твою історію настрою"

    return "💙 Я тебе слухаю. Розкажи більше"
