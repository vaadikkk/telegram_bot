import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# === Настройки ===
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise ValueError("❌ Переменная BOT_TOKEN не найдена в Environment Variables!")

# === Flask сервер (Для UptimeRobot) ===
# Этот сервер нужен, чтобы Render думал, что это веб-сайт,
# и чтобы UptimeRobot мог пинговать его снаружи.
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
    
    # drop_pending_updates=True помогает, если бот падал и накопил старые сообщения
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

# === Запуск ===
if __name__ == "__main__":
    # 1. Запускаем Flask в отдельном потоке (для UptimeRobot)
    threading.Thread(target=run_web, daemon=True).start()
    
    # 2. Запускаем самого бота в основном потоке
    # Мы убрали self_ping, так как он вызывал DDoS самого себя.
    # UptimeRobot справится с задачей "не давать уснуть" лучше.
    run_bot()
