import os
import openai
from dotenv import load_dotenv
from telegram import Update, Chat
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Load .env variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# ChatGPT function
async def chatgpt_response(message: str) -> str:
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",  # use "gpt-3.5-turbo" if you prefer cheaper option
            messages=[{"role": "user", "content": message}]
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

# Message handler
async def handle_group_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if message.chat.type in [Chat.GROUP, Chat.SUPERGROUP]:
        if message.text.lower().startswith('@CultSupreme_bot') or message.reply_to_message and message.reply_to_message.from_user.username == 'AI Supreme':
            user_text = message.text.replace('@CultSupreme_bot', '').strip()
            response = await chatgpt_response(user_text)
            await message.reply_text(response)

# Main app
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, handle_group_message))
    app.run_polling()