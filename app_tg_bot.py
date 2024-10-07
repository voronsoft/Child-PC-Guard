import os
import sys
import function
import asyncio
import logging
import threading
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler

# Глобальная переменная токена
TOKEN = function.read_data_json("bot_token_telegram")

# Глобальная переменная для приложения
application = None


# Включаем логирование для отладки
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

PID_FILE = "bot.pid"

# Правильный пароль
CORRECT_PASSWORD = function.get_password_from_registry()
# Словарь для хранения авторизованных пользователей
authorized_users = set(str(function.read_data_json("id_tg_bot_parent")))


def check_if_running():
    """Проверка, запущен ли бот уже, и завершение, если да."""
    if os.path.exists(PID_FILE):
        with open(PID_FILE, "r") as f:
            pid = int(f.read())
            if os.path.exists(f"/proc/{pid}"):
                print(f"Бот уже запущен с PID {pid}. Завершение.")
                sys.exit(1)

    # Записываем текущий PID в файл
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))


def remove_pid_file():
    """Удаление PID-файла при завершении."""
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)


async def shutdown(application):
    """Корректное завершение работы бота."""
    print("Остановка бота...")

    # Сначала останавливаем поллинг
    if application.updater is not None:
        application.updater.stop()  # Останавливаем поллинг

    # Ждем завершения оставшихся задач
    await application.stop()  # Функция, которая корректно завершает работу
    # Завершить текущий процесс
    os._exit(0)  # 0 обозначает успешное завершение
    sys.exit(0)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id

    await update.message.reply_text(f"Ваш chat_id: {chat_id}\n"
                                    f"Этот номер вам нужно ввести в программе - Child PC Guard\n"
                                    f"Нажав на кнопку в меню - 'Подключить оповещения через - Telegram'\n"
                                    f"Введите номер в поле для ввода и нажмите - ОК\n"
                                    f"После этого программа сможет понять кому отправлять сообщения"
                                    )

    # Проверяем, авторизован ли пользователь
    if chat_id not in authorized_users:
        await update.message.reply_text("Введите пароль для доступа:")
    else:
        await show_menu(update)


async def check_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id
    text = update.message.text

    # Если пользователь уже авторизован, показываем меню
    if chat_id in authorized_users:
        await handle_message(update, context)
        return

    # Проверяем пароль
    if function.check_password(text, CORRECT_PASSWORD):
        authorized_users.add(chat_id)
        await update.message.reply_text("Пароль верный! Доступ разрешен.")
        await show_menu(update)
    else:
        await update.message.reply_text("Неверный пароль. Попробуйте снова.")


async def show_menu(update: Update):
    keyboard = [
            [KeyboardButton("🔒 Заблокировать ПК"),
             KeyboardButton("🔓 Разблокировать ПК")],
            [KeyboardButton("💻 Выключить ПК"),
             KeyboardButton("⚠️ Вывести предупреждение")],
            [KeyboardButton("❌ Выключить приложение"),
             KeyboardButton("▶️ Включить приложение")],
            [KeyboardButton("⏲️ Выбрать время блокировки")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    await update.message.reply_text('Меню:', reply_markup=reply_markup)


async def choose_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
            [InlineKeyboardButton("1 час", callback_data='1'), InlineKeyboardButton("2 часа", callback_data='2')],
            [InlineKeyboardButton("3 часа", callback_data='3'), InlineKeyboardButton("4 часа", callback_data='4')],
            [InlineKeyboardButton("5 часов", callback_data='5')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите время для блокировки:', reply_markup=reply_markup)


async def handle_time_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    time_selected = query.data
    await query.message.reply_text(f"Вы выбрали: {time_selected.replace('_', ' ')} часа(ов) до блокировки.\n"
                                   f"Как только время выйдет, вы получите уведомление."
                                   )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat_id = update.message.chat.id

    # Проверяем, авторизован ли пользователь
    if chat_id not in authorized_users:
        await update.message.reply_text("Вы не авторизованы. Введите пароль.")
        return

    if text == "🔒 Заблокировать ПК":
        await update.message.reply_text("🔒 ПК заблокирован.")
    elif text == "🔓 Разблокировать ПК":
        await update.message.reply_text("🔓 ПК разблокирован.")
    elif text == "💻 Выключить ПК":
        await update.message.reply_text("💻 ПК выключен.")
    elif text == "⚠️ Вывести предупреждение":
        await update.message.reply_text("⚠️ Предупреждение выведено.")
    elif text == "❌ Выключить приложение":
        await update.message.reply_text("❌ Приложение выключено.")
    elif text == "▶️ Включить приложение":
        await update.message.reply_text("▶️ Приложение включено.")
    elif text == "⏲️ Выбрать время блокировки":
        await choose_time(update, context)
    elif text.lower() == "stop":  # Если получено сообщение "stop"
        await update.message.reply_text("🛑 Остановка бота...")

        remove_pid_file()  # Удаляем PID файл
        await shutdown(application)  # Остановка бота


async def main_bot_run():
    global application  # Объявляем application глобальной переменной

    # Проверяем, если бот уже запущен
    check_if_running()  # Проверяем перед запуском

    # Создаем приложение Telegram
    application = Application.builder().token(TOKEN).build()

    # Команда /start для запуска меню
    application.add_handler(CommandHandler("start", start))

    # Обработчик для проверки пароля
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_password))

    # Обработчик инлайн-кнопок
    application.add_handler(CallbackQueryHandler(handle_time_selection))

    # Запуск бота
    await application.initialize()  # Инициализация приложения
    await application.start()
    await application.updater.start_polling()

    # Ждем сигнала для завершения работы
    try:
        await asyncio.Event().wait()  # Это основной цикл, который ждет завершения
    except (KeyboardInterrupt, SystemExit):
        print("Остановка бота...")

    # Корректное завершение работы бота
    await shutdown(application)

    # Удаляем PID-файл при завершении
    remove_pid_file()  # Удаляем PID-файл при завершении


# --------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    # Запускаем бота
    asyncio.run(main_bot_run())
