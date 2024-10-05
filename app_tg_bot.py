import logging
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
from function import update_data_json, read_data_json

TOKEN = read_data_json("bot_token_telegram")

# Включаем логирование для отладки
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


# Функция для отображения главного меню с кнопками
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # После начала чата получаем id для того что бы бот мог отправлять пользователю сообщения из программы CPG
    chat_id = update.message.chat.id  # Получаем chat_id

    # Обновляем id в БД
    update_data_json("id_tg_bot_parent", chat_id)

    # Отправляем chat_id пользователю
    await update.message.reply_text(f"Ваш chat_id: {chat_id}")

    # Создаем основное меню с кнопками
    keyboard = [
            [KeyboardButton("🔒 Заблокировать ПК"),
             KeyboardButton("🔓 Разблокировать ПК")],
            [KeyboardButton("💻 Выключить ПК"),
             KeyboardButton("⚠️ Вывести предупреждение")],
            [KeyboardButton("❌ Выключить приложение")],
            [KeyboardButton("▶️ Включить приложение"),
             KeyboardButton("⏲️ Выбрать время блокировки")]
    ]

    # Отправляем сообщение с меню
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    await update.message.reply_text('Выберите действие для управления ПК:', reply_markup=reply_markup)


# Функция для выбора времени блокировки
async def choose_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Создаем инлайн-кнопки для выбора времени блокировки
    keyboard = [
            [InlineKeyboardButton("1 час", callback_data='1'),
             InlineKeyboardButton("2 часа", callback_data='2')],
            [InlineKeyboardButton("3 часа", callback_data='3'),
             InlineKeyboardButton("4 часа", callback_data='4')],
            [InlineKeyboardButton("5 часов", callback_data='5')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите время для блокировки:', reply_markup=reply_markup)


# Обработка нажатия на инлайн-кнопки
async def handle_time_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Подтверждение нажатия на кнопку

    # Получаем данные о выбранном времени
    time_selected = query.data
    await query.message.reply_text(f"Вы выбрали: {time_selected.replace('_', ' ')} часа(ов) до блокировки.\n"
                                   f"Как только время выйдет вы получите уведомлении о этом.")


# Обработка текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🔒 Заблокировать ПК":
        await update.message.reply_text("🔒 ПК заблокирован.")
    elif text == "🔓 Разблокировать ПК":
        await update.message.reply_text("🔓 ПК разблокирован.")
    elif text == "💻 Выключить ПК":
        await update.message.reply_text("💻 ПК выключен.")
    elif text == "⚠️ Вывести предупреждение":
        await update.message.reply_text("⚠️ Предупреждение выведено.")
    elif text == "📷 Включить камеру":
        await update.message.reply_text("📷 Камера включена.")
    elif text == "❌ Выключить приложение":
        await update.message.reply_text("❌ Приложение выключено.")
    elif text == "▶️ Включить приложение":
        await update.message.reply_text("▶️ Приложение включено.")
    elif text == "⏲️ Выбрать время блокировки":
        await choose_time(update, context)


# Основная функция для запуска бота
def main():
    # Создаем приложение Telegram
    application = Application.builder().token(TOKEN).build()

    # Команда /start для запуска меню
    application.add_handler(CommandHandler("start", start))

    # Обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Обработчик инлайн-кнопок
    application.add_handler(CallbackQueryHandler(handle_time_selection))

    # Запуск бота
    application.run_polling()


if __name__ == '__main__':
    main()
