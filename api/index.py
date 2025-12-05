import os
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# === Настройки ===
TOKEN = os.environ.get("BOT_TOKEN")

# Инициализируем FastAPI
app = FastAPI()

# === Логика бота ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Ваша логика осталась прежней
    await update.message.reply_text("👋 Привет! Теперь я работаю на Vercel через Webhook 🚀")

# === Подготовка приложения PTB ===
# Мы создаем application глобально, чтобы Vercel мог кэшировать его между запросами
ptb_application = Application.builder().token(TOKEN).build()
ptb_application.add_handler(CommandHandler("start", start))

@app.post("/")
async def process_update(request: Request):
    """
    Главная функция, которая принимает сообщения от Telegram
    """
    # 1. Получаем JSON из запроса
    data = await request.json()
    
    # 2. Превращаем JSON в объект Update
    update = Update.de_json(data, ptb_application.bot)
    
    # 3. Важный момент для serverless: нужно инициализировать приложение, 
    # если оно еще не готово (при холодном старте)
    async with ptb_application:
        # Обрабатываем обновление
        await ptb_application.process_update(update)

    return {"status": "ok"}

@app.get("/")
async def health_check():
    """Проверка, что сервер жив"""
    return {"status": "alive", "platform": "Vercel"}
