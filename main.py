import os
import requests
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

API_KEY = os.getenv("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")
BOT_TOKEN = os.getenv("8535999808:AAE0ax5gnJV_oLuvsSWODpqxSoVtf0A-d24")
WHOIS_API = os.getenv("qg3npLRBALiNjohfE5U0P1vXxyQ4WPM0ivv5u9At")

if not BOT_TOKEN:
    raise Exception("BOT_TOKEN missing")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚡ Bot Online")

async def panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("IP", callback_data="ip")]]
    await update.message.reply_text("Select:", reply_markup=InlineKeyboardMarkup(keyboard))

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["mode"] = query.data
    await query.message.reply_text("Send input")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Working")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("panel", panel))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

app.run_polling()