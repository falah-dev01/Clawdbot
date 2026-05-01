import os
import requests
import re
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

API_KEY = os.getenv("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")
BOT_TOKEN = os.getenv("8535999808:AAE0ax5gnJV_oLuvsSWODpqxSoVtf0A-d24")

app_web = Flask(__name__)

@app_web.route("/")
def home():
    return "Bot is running!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚡ Bot working")

async def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    await app.run_polling()

if __name__ == "__main__":
    import threading

    # run telegram bot in background
    threading.Thread(target=lambda: __import__("asyncio").run(run_bot())).start()

    # run web server (Render needs this)
    app_web.run(host="0.0.0.0", port=10000)