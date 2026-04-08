import os
import logging
import httpx
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:8000/ask")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [["/help", "/ask_legal"]]

    user_name = update.effective_user.first_name

    welcome_text = (
        f"Hello, {user_name}! 🇮🇪\n\n"
        "I am your Irish Immigration Assistant. I can help you with questions "
        "about visas, PPSN, housing, and stamps based on Citizens Information.\n\n"
        "How can I help you today?"
    )

    await update.message.reply_text(
        welcome_text,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    chat_id = update.effective_chat.id

    await context.bot.send_chat_action(chat_id=chat_id, action="typing")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                API_URL,
                json={"text": user_text},
                timeout=30.0
            )

        if response.status_code == 200:
            data = response.json()
            answer = data.get("answer", "No answer received.")
            sources = data.get("sources", [])

            source_links = "\n".join(
                [f"📍 [{s['title']}]({s['url']})" for s in sources if s['url'] != "#"]
            )

            full_response = f"{answer}\n\n*Sources:*\n{source_links}" if source_links else answer

            await update.message.reply_text(
                full_response,
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
        else:
            await update.message.reply_text("Sorry, I'm having trouble connecting to my brain. Try again later!")

    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("An error occurred while processing your request.")


def main():
    """Start the bot."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN not found in .env file")
        return

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Legal FAQ Bot is starting...")
    app.run_polling()


if __name__ == "__main__":
    main()