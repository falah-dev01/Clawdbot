# 🤖 Telegram AI Bot

A Claude-like Telegram bot powered by **OpenRouter** (any LLM), deployed free on **Render**.

---

## Stack

| Layer | Tool |
|-------|------|
| Bot framework | python-telegram-bot 21 |
| AI backend | OpenRouter API |
| Hosting | Render (free web service) |
| Language | Python 3.11+ |

---

## Quick Setup

### 1 — Get your keys

| Key | Where to get it |
|-----|----------------|
| `TELEGRAM_TOKEN` | [@BotFather](https://t.me/BotFather) → `/newbot` |
| `OPENROUTER_API_KEY` | [openrouter.ai/keys](https://openrouter.ai/keys) |

### 2 — Run locally (polling mode)

```bash
git clone <your-repo>
cd telegram-ai-bot

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# Edit .env — fill in TELEGRAM_TOKEN and OPENROUTER_API_KEY
# Leave WEBHOOK_URL empty for local polling

python bot.py
```

### 3 — Deploy to Render

1. Push this repo to GitHub.
2. Go to [render.com](https://render.com) → **New → Web Service** → connect your repo.
3. Render auto-detects `render.yaml`. Set these env vars in the dashboard:
   - `TELEGRAM_TOKEN`
   - `OPENROUTER_API_KEY`
   - `WEBHOOK_URL` → `https://<your-app-name>.onrender.com`
4. Deploy. Copy the Render URL.
5. Telegram will start receiving updates via webhook automatically.

> **Free tier note:** Render free services spin down after 15 min of inactivity.
> The first message after a cold start may take ~30 s. Upgrade to a paid plan to avoid this.

---

## Commands

| Command | Action |
|---------|--------|
| `/start` | Start a new session (clears history) |
| `/clear` | Clear your conversation history |
| `/model` | Show the active AI model |
| `/help` | Show help |

---

## Choosing a Model

Edit `MODEL` in your `.env` or Render env vars. Any OpenRouter model slug works:

```
# Free models
meta-llama/llama-3.1-8b-instruct:free
google/gemma-2-9b-it:free
mistralai/mistral-7b-instruct:free

# Paid Claude models
anthropic/claude-3.5-haiku        ← default (fast & cheap)
anthropic/claude-3.5-sonnet
anthropic/claude-opus-4
```

Full list: https://openrouter.ai/models

---

## Customising the Bot

- **System prompt** — change `SYSTEM_PROMPT` env var to give the bot a personality.
- **History length** — `MAX_HISTORY` controls how many messages are remembered per user.
- **Token limit** — edit `max_tokens` in `call_openrouter()` inside `bot.py`.
