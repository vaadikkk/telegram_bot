import threading
import http.server
import socketserver
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# 1️⃣ Функция для фиктивного HTTP-сервера
def fake_server():
    port = int(os.environ.get("PORT", 10000))  # Render передаёт порт сюда
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"🌐 Fake server running on port {port}")
        httpd.serve_forever()

# 2️⃣ Запускаем fake-server в отдельном потоке
threading.Thread(target=fake_server, daemon=True).start()

# 3️⃣ Основной код Telegram-бота
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привет! Я живу на Render и слушаю fake port 🌐")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Ты сказал: {update.message.text}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("✅ Telegram-бот запущен и работает в фоновом режиме...")
    app.run_polling()

if __name__ == "__main__":
    main()
