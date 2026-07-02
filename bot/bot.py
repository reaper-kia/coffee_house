import os
import asyncio
import logging
import re
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Константы рабочих часов кофейни
OPEN_HOUR = 8
CLOSE_HOUR = 22

# Данные для FAQ
FAQ_DATA = {
    "address": f"📍 **Адрес и часы работы**\n\nул. Кофейная, д. 10.\n⏰ Мы открыты каждый день с {OPEN_HOUR:02d}:00 до {CLOSE_HOUR:02d}:00.",
    "wifi": "🌐 **Пароль от Wi-Fi**\n\nСеть: `Coffee_Free_WiFi`\nПароль: `I_Love_Espresso2026`",
    "milk": "🥛 **Альтернативное молоко**\n\nДобавим в любой напиток:\n• Овсяное, Кокосовое, Миндальное (+50₽)"
}

class BookingSteps(StatesGroup):
    waiting_for_date = State()    
    waiting_for_time = State()    
    waiting_for_guests = State()  

def main_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🛍 Сделать предзаказ", web_app=types.WebAppInfo(url="https://google.com")))
    builder.row(types.InlineKeyboardButton(text="📅 Забронировать стол", callback_data="start_booking"))
    builder.row(types.InlineKeyboardButton(text="ℹ️ Частые вопросы (FAQ)", callback_data="btn_faq"))
    return builder.as_markup()

@dp.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text=f"Привет, {message.from_user.first_name}! ☕️\nВыберите действие:",
        reply_markup=main_menu_keyboard()
    )

# ================= МЕНЮ FAQ =================
@dp.callback_query(F.data == "btn_faq")
async def show_faq(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="📍 Адрес", callback_data="faq_address"))
    builder.row(types.InlineKeyboardButton(text="🌐 Wi-Fi", callback_data="faq_wifi"))
    builder.row(types.InlineKeyboardButton(text="🥛 Молоко", callback_data="faq_milk"))
    builder.row(types.InlineKeyboardButton(text="« Назад", callback_data="go_to_main"))
    await callback.message.edit_text(text="ℹ️ **Частые вопросы.** Что вас интересует?", reply_markup=builder.as_markup(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data.startswith("faq_"))
async def show_faq_answer(callback: types.CallbackQuery):
    topic = callback.data.split("_")[1]
    await callback.message.edit_text(
        text=FAQ_DATA.get(topic, "Ошибка."), 
        reply_markup=InlineKeyboardBuilder().row(types.InlineKeyboardButton(text="« Назад в FAQ", callback_data="btn_faq")).as_markup(), 
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(F.data == "go_to_main")
async def go_back_main(callback: types.CallbackQuery):
    await callback.message.edit_text(text="Выберите действие:", reply_markup=main_menu_keyboard())
    await callback.answer()


# ================= БРОНИРОВАНИЕ С ВАЛИДАЦИЕЙ И КНОПКАМИ ДАТЫ =================

# 1. НАЧАЛО БРОНИРОВАНИЯ (Кнопки + Текст)
@dp.callback_query(F.data == "start_booking")
async def book_table_start(callback: types.CallbackQuery, state: FSMContext):
    # Генерируем даты для кнопок динамически
    today_str = datetime.now().strftime("%d.%m.%Y")
    tomorrow_str = (datetime.now() + timedelta(days=1)).strftime("%d.%m.%Y")
    
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=f"Сегодня ({today_str[:-5]})", callback_data=f"bookdate_{today_str}"))
    builder.row(types.InlineKeyboardButton(text=f"Завтра ({tomorrow_str[:-5]})", callback_data=f"bookdate_{tomorrow_str}"))
    
    await callback.message.edit_text(
        text="📅 Шаг 1 из 3: Выбор даты\n\n"
             "Нажмите на кнопку Сегодня / Завтра или отправьте любую другую дату сообщением в формате ДД.ММ.ГГГГ (например, 15.07.2026):",
        reply_markup=builder.as_markup()
    )
    await state.set_state(BookingSteps.waiting_for_date)
    await callback.answer()

# Вспомогательная функция для проверки даты
def validate_and_format_date(date_text: str) -> str or None:
    try:
        input_date = datetime.strptime(date_text, "%d.%m.%Y").date()
        if input_date < datetime.now().date():
            return "past"
        return date_text
    except ValueError:
        return None

# 1.1 Перехват ДАТЫ, если пользователь НАЖАЛ НА КНОПКУ
@dp.callback_query(BookingSteps.waiting_for_date, F.data.startswith("bookdate_"))
async def book_table_date_callback(callback: types.CallbackQuery, state: FSMContext):
    chosen_date = callback.data.split("_")[1]
    await state.update_data(date=chosen_date)
    
    await callback.message.edit_text(
        text=f"✅ Дата принята: {chosen_date}\n\n"
             f"⏰ Шаг 2 из 3: Выбор времени\n"
             f"Кофейня работает с {OPEN_HOUR:02d}:00 до {CLOSE_HOUR:02d}:00.\n"
             f"Напишите желаемое время в формате ЧЧ:ММ (например, 18:30):",
        parse_mode="Markdown"
    )
    await state.set_state(BookingSteps.waiting_for_time)
    await callback.answer()

# 1.2 Перехват ДАТЫ, если пользователь НАПИСАЛ ЕЁ ТЕКСТОМ
@dp.message(BookingSteps.waiting_for_date)
async def book_table_date_message(message: types.Message, state: FSMContext):
    result = validate_and_format_date(message.text.strip())
    
    if result == "past":
        await message.answer("❌ Эта дата уже в прошлом! Напишите актуальную дату:")
        return
    elif result is None:
        await message.answer("❌ Неверный формат! Напишите дату строго в формате ДД.ММ.ГГГГ (например, 20.08.2026):")
        return
        
    await state.update_data(date=result)
    await message.answer(
        text=f"✅ Дата принята: *{result}*\n\n"
             f"⏰ Шаг 2 из 3: Выбор времени\n"
             f"Мы открыты с {OPEN_HOUR:02d}:00 до {CLOSE_HOUR:02d}:00.\n"
             f"Напишите время визита в формате ЧЧ:ММ (например, 14:00):",
        parse_mode="Markdown"
    )
    await state.set_state(BookingSteps.waiting_for_time)

# 2. ПРОВЕРКА ВРЕМЕНИ И РАБОЧИХ ЧАСОВ
@dp.message(BookingSteps.waiting_for_time)
async def book_table_time(message: types.Message, state: FSMContext):
    user_time = message.text.strip()
    
    # Регулярка проверки базового формата ЧЧ:ММ
    if not re.match(r"^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$", user_time):
        await message.answer("❌ Неверный формат времени! Напишите время в виде ЧЧ:ММ (например, 16:15):")
        return
        
    # Бьем строчку времени на часы и минуты
    hours, minutes = map(int, user_time.split(":"))
    
    # ПРОВЕРКА: Входит ли время в рабочие часы кофейни (8:00 - 22:00)
    # Если время ровно 22:00 - это край, позже нельзя
    if hours < OPEN_HOUR or hours > CLOSE_HOUR or (hours == CLOSE_HOUR and minutes > 0):
        await message.answer(
            f"❌ Кофейня в это время закрыта!\n"
            f"Пожалуйста, выберите время в диапазоне работы: с {OPEN_HOUR:02d}:00 до {CLOSE_HOUR:02d}:00."
        )
        return
        
    await state.update_data(time=user_time)
    await message.answer(text="👥 Шаг 3 из 3: Количество гостей\n\nНапишите числом, сколько человек будет (от 1 до 10):")
    await state.set_state(BookingSteps.waiting_for_guests)

# 3. ПРОВЕРКА ГОСТЕЙ И ФИНАЛ
@dp.message(BookingSteps.waiting_for_guests)
async def book_table_finish(message: types.Message, state: FSMContext):
    user_guests = message.text.strip()
    
    if not user_guests.isdigit() or not (1 <= int(user_guests) <= 10):
        await message.answer("❌ Пожалуйста, укажите реальное число гостей от 1 до 10 человек:")
        return
        
    user_data = await state.get_data()
    
    summary_text = (
        f"🎉 **Бронирование успешно оформлено!**\n\n"
        f"👤 Имя: {message.from_user.first_name}\n"
        f"📅 Дата: {user_data['date']}\n"
        f"⏰ Время: {user_data['time']}\n"
        f"👥 Число гостей: {user_guests} чел.\n\n"
        f"Ждем вас в гости! Нажмите /start, чтобы вернуться в меню."
    )
    
    await message.answer(text=summary_text, parse_mode="Markdown", reply_markup=main_menu_keyboard())
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())