from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

# Токен твоего бота
TOKEN = "7607383287:AAFPQatV3NC-xnUe_GRtBoPI0-OWRDS4ucs"

# Твой Telegram numeric ID (куда пересылать сообщения)
ADMIN_ID = 369596135

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напиши сюда сообщение, и я передам его админу.")

# Пересылка всех текстовых сообщений админу
async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    user = update.message.from_user
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"Сообщение от @{user.username or user.id}:\n{message}"
    )
    await update.message.reply_text("Сообщение отправлено админу. Спасибо!")

# Запуск бота
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_to_admin))

app.run_polling()
