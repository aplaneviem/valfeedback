from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
import os

TOKEN = "7607383287:AAFPQatV3NC-xnUe_GRtBoPI0-OWRDS4ucs"
ADMIN_ID = 369596135

# Для хранения активного ответа
pending_replies = {}

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напиши сюда сообщение, и я передам его админу.")

# Пересылка сообщений от пользователей админу
async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id == ADMIN_ID:
        return  # Не пересылаем сообщения от админа

    user = update.message.from_user
    text = update.message.text
    user_id = user.id
    username = user.username or f"{user.first_name} {user.last_name or ''}".strip()

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Ответить", callback_data=f"reply:{user_id}")]
    ])

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📩 Сообщение от @{username} (ID: {user_id}):\n{text}",
        reply_markup=keyboard
    )

    await update.message.reply_text("Сообщение отправлено админу. Спасибо!")

# Обработка нажатия на кнопку "Ответить"
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.from_user.id != ADMIN_ID:
        await query.edit_message_text("У вас нет прав.")
        return

    _, user_id = query.data.split(":")
    pending_replies[ADMIN_ID] = int(user_id)
    await context.bot.send_message(chat_id=ADMIN_ID, text="✏️ Напиши сообщение для отправки пользователю.")

# Обработка ответа админа пользователю
async def handle_admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return  # Не обрабатываем, если не админ

    if ADMIN_ID in pending_replies:
        target_id = pending_replies.pop(ADMIN_ID)
        try:
            await context.bot.send_message(chat_id=target_id, text=update.message.text)
            await update.message.reply_text("✅ Ответ отправлен.")
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка отправки: {e}")
    else:
        await update.message.reply_text("❗ Сначала нажмите кнопку 'Ответить' под сообщением.")

# Запуск бота
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_callback))
app.add_handler(MessageHandler(filters.TEXT & filters.User(ADMIN_ID), handle_admin_reply))
app.add_handler(MessageHandler(filters.TEXT & ~filters.User(ADMIN_ID) & ~filters.COMMAND, forward_to_admin))

app.run_polling()

