import os
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime

# Получаем токен и ID из переменных окружения Railway
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Храним чаты внутри бота
chats = [
    {"name": "Ейск — чат жителей", "link": "https://t.me/Yeysk193"},
    {"name": "Ейск объявления", "link": "https://t.me/eysk_ads"},
    {"name": "Ейск ЧП/ДТП", "link": "https://t.me/eysk_incidents"},
]

# История отправок
history = {}

# Шаблоны приглашений
templates = {
    "1": "Привет! Запустил новый локальный канал «Ейск Пульс» — архив, ностальгия, редкие фото города. Буду рад, если заглянешь.",
    "2": "Нашёл архивные фото Ейска 2000‑х. Собираю коллекцию и делюсь в канале «Ейск Пульс». Присоединяйся.",
    "3": "Если у тебя есть старые фото Ейска — присылай! Мы собираем историю города. Канал: Ейск Пульс.",
    "4": "Локальный проект «Ейск Пульс» — архив, редкие фото, история города. Без политики и спама. Подписывайтесь.",
    "5": "Если любишь Ейск и ностальгию — тебе сюда: Ейск Пульс."
}

# Главное меню
def main_menu():
    kb = InlineKeyboardBuilder()
    kb.button(text="📂 Список чатов", callback_data="show_chats")
    kb.button(text="📝 Шаблоны приглашений", callback_data="show_templates")
    kb.button(text="📊 История отправок", callback_data="show_history")
    kb.adjust(1)
    return kb.as_markup()

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Бот‑ассистент «Ейск Пульс» готов работать.", reply_markup=main_menu())

# Показ списка чатов
@dp.callback_query(F.data == "show_chats")
async def show_chats(callback: CallbackQuery):
    kb = InlineKeyboardBuilder()
    for i, chat in enumerate(chats):
        kb.button(text=chat["name"], callback_data=f"chat_{i}")
    kb.button(text="⬅️ Назад", callback_data="back")
    kb.adjust(1)
    await callback.message.edit_text("Выбери чат:", reply_markup=kb.as_markup())

# Открытие чата
@dp.callback_query(F.data.startswith("chat_"))
async def open_chat(callback: CallbackQuery):
    index = int(callback.data.split("_")[1])
    chat = chats[index]

    history[chat["name"]] = datetime.now().strftime("%Y-%m-%d %H:%M")

    kb = InlineKeyboardBuilder()
    kb.button(text="Открыть чат", url=chat["link"])
    kb.button(text="⬅️ Назад", callback_data="show_chats")
    kb.adjust(1)

    await callback.message.edit_text(
        f"Чат: {chat['name']}\n\n"
        f"Последняя отправка: {history.get(chat['name'], '—')}",
        reply_markup=kb.as_markup()
    )

# Показ шаблонов
@dp.callback_query(F.data == "show_templates")
async def show_templates(callback: CallbackQuery):
    kb = InlineKeyboardBuilder()
    for key in templates:
        kb.button(text=f"Шаблон {key}", callback_data=f"template_{key}")
    kb.button(text="⬅️ Назад", callback_data="back")
    kb.adjust(1)
    await callback.message.edit_text("Выбери шаблон:", reply_markup=kb.as_markup())

# Показ текста шаблона
@dp.callback_query(F.data.startswith("template_"))
async def show_template(callback: CallbackQuery):
    key = callback.data.split("_")[1]
    text = templates[key]

    kb = InlineKeyboardBuilder()
    kb.button(text="⬅️ Назад", callback_data="show_templates")
    kb.adjust(1)

    await callback.message.edit_text(
        f"Шаблон {key}:\n\n{text}\n\nСкопируй и вставь в чат.",
        reply_markup=kb.as_markup()
    )

# История отправок
@dp.callback_query(F.data == "show_history")
async def show_history(callback: CallbackQuery):
    if not history:
        text = "История пока пуста."
    else:
        text = "📊 История отправок:\n\n"
        for chat, date in history.items():
            text += f"• {chat}: {date}\n"

    kb = InlineKeyboardBuilder()
    kb.button(text="⬅️ Назад", callback_data="back")
    kb.adjust(1)

    await callback.message.edit_text(text, reply_markup=kb.as_markup())

# Назад
@dp.callback_query(F.data == "back")
async def go_back(callback: CallbackQuery):
    await callback.message.edit_text("Главное меню:", reply_markup=main_menu())

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
