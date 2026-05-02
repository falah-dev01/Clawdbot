import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler

BOT_TOKEN ="8752843871:AAGqNZ6d0XhVwKkMVQDA-GTWl5xlrOFSLK0"
WEBHOOK_URL ="https://clawdbot-5w1n.onrender.com"

bot = Bot(token=BOT_TOKEN)
app = Flask(__name__)
dispatcher = Dispatcher(bot, None, use_context=True)

# --- command ---
def start(update, context):
    update.message.reply_text("⚡ Webhook bot working!")

dispatcher.add_handler(CommandHandler("start", start))

# --- webhook route ---
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot)
    dispatcher.process_update(update)
    return "ok"

# --- home route ---
@app.route("/")
def home():
    return "Webhook bot is running"

# --- start ---
if __name__ == "__main__":
    if not BOT_TOKEN:
        raise Exception("BOT_TOKEN missing")

    # set webhook
    bot.set_webhook(url=f"{WEBHOOK_URL}/{BOT_TOKEN}")

    app.run(host="0.0.0.0", port=10000)
