def run_agent(user_message: str, thread_id: str = ""):

    msg = user_message.lower()

    if "погано" in msg:
        return "💙 Я поруч. Це нормально так почуватися."

    if "стрес" in msg:
        return "🌿 Спробуй зробити паузу і відпочити."

    if "що робити" in msg:
        return "✨ Прогулянка, вода і сон дуже допомагають."

    if "привіт" in msg:
        return "👋 Привіт! Як ти себе почуваєш?"

    if "настрій" in msg:
        return "📊 Я бачу, ти говориш про свій стан. Розкажи більше."

    return "💬 Я тебе слухаю. Продовжуй."
