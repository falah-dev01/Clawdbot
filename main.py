import os
import threading
import asyncio
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN ="8752843871:AAGqNZ6d0XhVwKkMVQDA-GTWl5xlrOFSLK0"

# --- Simple web server (Render needs this) ---
web = Flask(__name__)

@web.route("/")
def home():
    return "Bot is running"

# --- Telegram handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚡ Bot working!")

# --- Run bot (polling) ---
async def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    await app.initialize()
    await app.start()
    await app.bot.initialize()

    # THIS is the important line:
    await app.run_polling()

def start_bot():
    asyncio.run(run_bot())

# --- Start both ---
if __name__ == "__main__":
    if not BOT_TOKEN:
        raise Exception("BOT_TOKEN missing")

    threading.Thread(target=start_bot).start()
    web.run(host="0.0.0.0", port=10000)
    # Start Telegram bot in background
    threading.Thread(target=start_bot).start()

    # Start web server (Render needs this)
    app_web.run(host="0.0.0.0", port=10000)