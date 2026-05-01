import os
import asyncio
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN ="8752843871:AAG1jOpUlzjZSyBqOFGBTho82xHBZ9flnjk"

app_web = Flask(__name__)

@app_web.route("/")
def home():
    return "Bot is running"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚡ Bot working!")

async def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    await app.initialize()
    await app.start()
    await app.updater.start_polling()

def start_bot():
    asyncio.run(run_bot())

if __name__ == "__main__":
    import threading

    # Start Telegram bot in background
    threading.Thread(target=start_bot).start()

    # Start web server (Render needs this)
    app_web.run(host="0.0.0.0", port=10000)