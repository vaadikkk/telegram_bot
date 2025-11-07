from telegram.ext import Updater, CommandHandler
import os

# Берем токен из переменных окружения Render
TOKEN = os.environ.get("BOT_TOKEN")

def start(update, context):
    update.message.reply_text("Привет! Я работаю 24/7 на Render 🚀")

def help_command(update, context):
    update.message.reply_text("Напиши /start, чтобы проверить, что я онлайн.")

updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("help", help_command))

updater.start_polling()
updater.idle()
