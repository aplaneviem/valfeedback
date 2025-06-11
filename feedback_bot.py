from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напиши сюда сообщение, и я передам его админу.")

async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    user = update.message.from_user
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"Сообщение от @{user.username or user.id}:
{message}"
    )
    await update.message.reply_text("Сообщение отправлено админу. Спасибо!")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_to_admin))

app.run_polling()
