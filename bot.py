import os
import threading
import requests
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# === Настройки ===
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise ValueError("❌ Переменная BOT_TOKEN не найдена в Environment Variables!")

# === Flask сервер ===
web_app = Flask(__name__)

@web_app.route("/")
def home():
    return "✅ Telegram bot is alive and responding", 200

def run_web():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host="0.0.0.0", port=port)

# === Telegram бот ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привет! Я современный Telegram-бот на Render 🚀")

def run_bot():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("🤖 Бот запущен и слушает Telegram...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

# === Периодический self-ping, чтобы Render не засыпал ===
def self_ping():
    url = "https://telegram-bot-gvyt.onrender.com"
    while True:
        try:
            requests.get(url)
            print("🔄 Self-ping:", url)
        except Exception as e:
            print("⚠️ Self-ping error:", e)
        import time; time.sleep(600)  # каждые 10 минут

# === Запуск всех потоков ===
if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    threading.Thread(target=self_ping).start()
    run_bot()
