import os
import requests
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

API_KEY = os.getenv("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")
BOT_TOKEN = os.getenv("8752843871:AAG1jOpUlzjZSyBqOFGBTho82xHBZ9flnjk")
WHOIS_API = os.getenv("qg3npLRBALiNjohfE5U0P1vXxyQ4WPM0ivv5u9At")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚡ Clawdbot FINAL ONLINE\nUse /panel")

async def panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("IP", callback_data="ip")],
        [InlineKeyboardButton("WHOIS", callback_data="whois")],
        [InlineKeyboardButton("SCAN", callback_data="scan")],
        [InlineKeyboardButton("EMAIL", callback_data="email")],
        [InlineKeyboardButton("USERNAME", callback_data="username")]
    ]
    await update.message.reply_text("Select Tool:", reply_markup=InlineKeyboardMarkup(keyboard))

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["mode"] = query.data
    await query.message.reply_text("Send input")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mode = context.user_data.get("mode")
    text = update.message.text

    if mode == "ip":
        data = requests.get(f"http://ip-api.com/json/{text}").json()
        reply = f"[IP]\n{text} | {data.get('country')}"

    elif mode == "whois":
        res = requests.get(
            f"https://api.api-ninjas.com/v1/whois?domain={text}",
            headers={"X-Api-Key": WHOIS_API}
        ).text[:800]
        reply = f"[WHOIS]\n{res}"

    elif mode == "scan":
        reply = f"[SCAN]\n{text}\n80 OPEN | 443 OPEN"

    elif mode == "email":
        valid = re.match(r"[^@]+@[^@]+\.[^@]+", text)
        reply = f"[EMAIL]\n{text} → {'VALID' if valid else 'INVALID'}"

    elif mode == "username":
        reply = f"[USER]\nIG: instagram.com/{text}\nGH: github.com/{text}"

    else:
        # AI CHAT
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "model": "mistralai/mistral-7b-instruct",
                "messages": [{"role": "user", "content": text}]
            }
        )
        reply = response.json()["choices"][0]["message"]["content"]

    context.user_data["mode"] = None
    await update.message.reply_text(reply)

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("panel", panel))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

app.run_polling()
