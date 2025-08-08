import os
import random
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from datetime import datetime

# Получаем токен и ID канала из переменных окружения
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# База карт Таро
cards = [
    {
        "name": "Шут",
        "description": "Новые начинания, свобода, спонтанность.",
        "image": "images/shut.jpg"
    },
    {
        "name": "Маг",
        "description": "Власть, умение, создание реальности.",
        "image": "images/mag.jpg"
    },
    {
        "name": "Верховная Жрица",
        "description": "Интуиция, тайна, внутреннее знание.",
        "image": "images/zhritsa.jpg"
    }
]

# Функция для выбора карты дня
def card_of_the_day():
    day_of_year = datetime.now().timetuple().tm_yday
    return cards[day_of_year % len(cards)]

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напиши /подсказка или /картадня, чтобы получить карту Таро.")

# Команда /подсказка
async def hint(update: Update, context: ContextTypes.DEFAULT_TYPE):
    card = random.choice(cards)
    with open(card["image"], "rb") as img:
        await update.message.reply_photo(photo=InputFile(img), caption=f"{card['name']}\n{card['description']}")

# Команда /картадня
async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    card = card_of_the_day()
    with open(card["image"], "rb") as img:
        await update.message.reply_photo(photo=InputFile(img), caption=f"{card['name']}\n{card['description']}")

# Авто-отправка карты дня в канал
async def send_daily_card(app):
    card = card_of_the_day()
    with open(card["image"], "rb") as img:
        await app.bot.send_photo(chat_id=CHANNEL_ID, photo=InputFile(img), caption=f"Карта дня:\n{card['name']}\n{card['description']}")

# Запуск бота
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("подсказка", hint))
    app.add_handler(CommandHandler("картадня", today))

    app.run_polling()
