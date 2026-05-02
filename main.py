import os
import threading
import asyncio
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("8752843871:AAGqNZ6d0XhVwKkMVQDA-GTWl5xlrOFSLK0")

web = Flask(__name__)

@web.route("/")
def home():
    return "Bot is running"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("MESSAGE RECEIVED")  # debug
    await update.message.reply_text("⚡ Bot working!")

async def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    await app.initialize()
    await app.start()
    await app.run_polling()

def start_bot():
    asyncio.run(run_bot())

if __name__ == "__main__":
    if not BOT_TOKEN:
        raise Exception("BOT_TOKEN missing")

    threading.Thread(target=start_bot).start()
    web.run(host="0.0.0.0", port=10000)
