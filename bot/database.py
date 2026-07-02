import asyncio

# FAQ 
FAQ_DATA = {
    "address": (
        "📍 **Адрес и часы работы**\n\n"
        "ул. Кофейная, д. 10.\n"
        "⏰ Мы открыты каждый день с 08:00 до 22:00."
    ),
    "wifi": (
        "🌐 **Пароль от Wi-Fi**\n\n"
        "Сеть: `Coffee_Free_WiFi`\n"
        "Пароль: `I_Love_Espresso2026`"
    ),
    "milk": (
        "🥛 **Альтернативное молоко**\n\n"
        "Добавим в любой напиток:\n"
        "• Овсяное, Кокосовое, Миндальное (+50₽)"
    )
}


async def send_booking_to_server(user_id: int):
    await asyncio.sleep(0.5)  
    return {"status": "success", "booking_id": 999}