import os
import logging
import httpx
from telegram import Update, BotCommand
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from telegram.constants import ChatAction

# ── Logging ────────────────────────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ── Config ─────────────────────────────────────────────────────────────────
TELEGRAM_TOKEN   = os.environ["TELEGRAM_TOKEN"]
OPENROUTER_KEY   = os.environ["OPENROUTER_API_KEY"]
MODEL            = os.environ.get("MODEL", "anthropic/claude-3.5-haiku")
WEBHOOK_URL      = os.environ.get("WEBHOOK_URL", "")          # e.g. https://your-app.onrender.com
PORT             = int(os.environ.get("PORT", 8443))
MAX_HISTORY      = int(os.environ.get("MAX_HISTORY", 20))     # messages kept per user
SYSTEM_PROMPT    = os.environ.get(
    "SYSTEM_PROMPT",
    "You are a helpful, harmless, and honest AI assistant. "
    "Be concise, clear, and friendly. Use Markdown when it helps readability.",
)

OPENROUTER_URL   = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": WEBHOOK_URL or "https://telegram-ai-bot",
    "X-Title": "Telegram AI Bot",
}

# ── In-memory conversation store: {user_id: [{"role": ..., "content": ...}]}
conversations: dict[int, list[dict]] = {}


def get_history(user_id: int) -> list[dict]:
    return conversations.setdefault(user_id, [])


def trim_history(user_id: int) -> None:
    history = conversations.get(user_id, [])
    if len(history) > MAX_HISTORY:
        conversations[user_id] = history[-MAX_HISTORY:]


# ── OpenRouter call ────────────────────────────────────────────────────────
async def call_openrouter(messages: list[dict]) -> str:
    payload = {
        "model": MODEL,
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + messages,
        "max_tokens": 1024,
        "temperature": 0.7,
    }
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(OPENROUTER_URL, headers=OPENROUTER_HEADERS, json=payload)
        resp.raise_for_status()
        data = resp.json()
    return data["choices"][0]["message"]["content"]


# ── Handlers ───────────────────────────────────────────────────────────────
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    conversations.pop(user.id, None)          # fresh session
    await update.message.reply_text(
        f"👋 Hey *{user.first_name}*! I'm your AI assistant powered by *{MODEL}*.\n\n"
        "Just send me a message and I'll reply. Use /help for commands.",
        parse_mode="Markdown",
    )


async def help_cmd(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "*Commands*\n"
        "/start  — Start a new chat session\n"
        "/clear  — Clear your conversation history\n"
        "/model  — Show the current AI model\n"
        "/help   — Show this message",
        parse_mode="Markdown",
    )


async def clear_cmd(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    conversations.pop(update.effective_user.id, None)
    await update.message.reply_text("🗑️ Conversation cleared. Fresh start!")


async def model_cmd(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"🤖 Current model: `{MODEL}`", parse_mode="Markdown")


async def handle_message(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    user_id   = update.effective_user.id
    user_text = update.message.text.strip()

    if not user_text:
        return

    # Show typing indicator
    await ctx.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.TYPING
    )

    history = get_history(user_id)
    history.append({"role": "user", "content": user_text})

    try:
        reply = await call_openrouter(history)
    except httpx.HTTPStatusError as e:
        logger.error("OpenRouter HTTP error: %s", e)
        await update.message.reply_text("⚠️ API error. Please try again.")
        history.pop()   # remove failed user message
        return
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        await update.message.reply_text("⚠️ Something went wrong. Please try again.")
        history.pop()
        return

    history.append({"role": "assistant", "content": reply})
    trim_history(user_id)

    # Telegram caps messages at 4096 chars — split if needed
    for chunk in [reply[i:i+4000] for i in range(0, len(reply), 4000)]:
        await update.message.reply_text(chunk, parse_mode="Markdown")


# ── App bootstrap ──────────────────────────────────────────────────────────
def main() -> None:
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help",  help_cmd))
    app.add_handler(CommandHandler("clear", clear_cmd))
    app.add_handler(CommandHandler("model", model_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    if WEBHOOK_URL:
        # ── Webhook mode (Render) ──────────────────────────────────────────
        logger.info("Starting webhook on port %d …", PORT)
        app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=TELEGRAM_TOKEN,
            webhook_url=f"{WEBHOOK_URL}/{TELEGRAM_TOKEN}",
        )
    else:
        # ── Polling mode (local dev) ───────────────────────────────────────
        logger.info("Starting polling …")
        app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
