import os
import sys
import ctypes
import asyncio
import logging
import function
import config_localization
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler

#

# Подключаем локализацию
_ = config_localization.setup_locale(function.read_data_json("language"))

# Имя мьютекса (должно быть уникальным)
MUTEX_NAME_BCPG = "Global\\BOT_Child_PC"

# Глобальная переменная токена
TOKEN = function.read_data_json("bot_token_telegram")

# Объявляем переменную глобально
mutex = None

# Включаем логирование для отладки
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Правильный пароль
CORRECT_PASSWORD = function.get_password_from_registry()
# Словарь для хранения авторизованных пользователей
authorized_users = set()


# Корректное завершение работы бота.
async def shutdown(application, mutex):
    """Корректное завершение работы бота."""
    # Закрытие мьютекса при завершении приложения
    if mutex is not None and mutex != 0:
        ctypes.windll.kernel32.CloseHandle(mutex)

    # Сначала останавливаем поллинг
    if application.updater is not None:
        application.updater.stop()  # Останавливаем поллинг

    # Ждем завершения оставшихся задач
    await application.stop()  # Функция, которая корректно завершает работу
    # Завершить текущий процесс
    os._exit(0)  # 0 обозначает успешное завершение


# Запуск бота
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запуск бота"""
    chat_id = update.message.chat.id

    await update.message.reply_text(_("Ваш chat_id: {chat_id}\nЭтот номер вам нужно ввести в программе - Child PC Guard\n"
                                      "Нажав на кнопку в меню - 'Подключить оповещения через - Telegram'\n"
                                      "Введите номер в поле для ввода и нажмите - ОК\n"
                                      "После этого программа сможет понять кому отправлять сообщения"
                                      ).format(chat_id=chat_id)
                                    )

    # Проверяем, авторизован ли пользователь
    if chat_id not in authorized_users:
        await update.message.reply_text(_("Введите пароль для доступа\n(тот который вы вводили в программе):"))
    else:
        await show_menu(update)


# Проверка пароля
async def check_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Проверка пароля"""
    # ID чата
    chat_id = update.message.chat.id
    #
    text = update.message.text

    # Если пользователь уже авторизован, показываем меню
    if chat_id in authorized_users:
        await handle_message(update, context)
        return

    # Проверяем пароль
    if function.check_password(text, CORRECT_PASSWORD):
        # Записываем пользователя в список разрешенных пользователей
        answer = function.update_data_json("id_tg_bot_parent", chat_id)
        if answer:
            authorized_users.add(chat_id)

        await update.message.reply_text(_("Доступ разрешен."))
        await show_menu(update)
    else:
        await update.message.reply_text(_("Неверный пароль. Попробуйте снова."))


# Отображение меню кнопок
async def show_menu(update: Update):
    """Отображение меню кнопок"""
    keyboard = [
            [KeyboardButton(_("Получить статус CPG")), KeyboardButton(_("Вывести предупреждение"))],
            [KeyboardButton(_("Выключить ПК")), KeyboardButton(_("Разблокировать ПК"))],
            [KeyboardButton(_("Выбрать время для блокировки"))]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    await update.message.reply_text(_("Меню:"), reply_markup=reply_markup)


# Выбор времени для блокировки
async def choose_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Выбор времени для блокировки"""
    keyboard = [
            [InlineKeyboardButton(_("1 час"), callback_data='1'), InlineKeyboardButton(_("2 часа"), callback_data='2')],
            [InlineKeyboardButton(_("3 часа"), callback_data='3'), InlineKeyboardButton(_("4 часа"), callback_data='4')],
            [InlineKeyboardButton(_("5 часов"), callback_data='5')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(_("Выберите время для блокировки:"), reply_markup=reply_markup)


async def handle_time_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """"""
    query = update.callback_query
    await query.answer()
    time_selected = query.data
    time_to_sec = int(query.data) * 3600

    message_text = (_("Вы выбрали: {time_selected} часа(ов) до блокировки.\nТаймер начал отсчет времени!\n"
                      "Как только время выйдет, вы получите уведомление."
                      ).format(time_selected=time_selected.replace('_', ' ')))
    await query.message.reply_text(message_text)


# Обработка сообщения с предупреждением
async def handle_warning_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка ввода текста для предупреждения."""
    # Получаем текст сообщения от пользователя
    text = update.message.text

    # Вывод устрашающего предупреждения на экран
    function.show_message_with_auto_close(message=text, delay=30)
    await update.message.reply_text(_("Устрашающее сообщение выведено на главном экране."))


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка сообщений от пользователя."""
    text = update.message.text
    chat_id = update.message.chat.id
    # ------------------------------
    time_bd = function.read_data_json("remaining_time")
    time = function.seconds_to_hms(time_bd)

    status_prg = function.check_if_program_running("Child PC Guard.exe")

    # Имя пользователя для кого назначена блокировка
    username_block = function.read_data_json("username_blocking")

    status_bot = function.read_data_json("id_tg_bot_parent")

    # Проверяем, авторизован ли пользователь
    if chat_id not in authorized_users:
        await update.message.reply_text(_("Вы не авторизованы. Введите пароль."))
        return

    if text == _("Вывести предупреждение"):
        await update.message.reply_text(_("Пожалуйста, введите текст для сообщения."))
        # Сохраняем состояние, чтобы обрабатывать следующий ввод
        context.user_data['waiting_for_warning'] = True
    else:
        # Проверяем, ожидает ли бот текст для предупреждения
        if context.user_data.get('waiting_for_warning'):
            await handle_warning_message(update, context)
            # Сбрасываем состояние
            context.user_data['waiting_for_warning'] = False
            return

    if text == _("Получить статус CPG"):
        # await update.message.reply_text(f"{_("СТАТУС ПРОГРАММЫ:\n- CPG:")} {_("Работает") if status_prg else _("Выключено")}\n{_("- Пользователь:")} {username_block if len(username_block) else _("Не найдено")}\n{_("- Таймер:")} {time if time else _("Не включено")}\n{_("- Оповещение Telegram:")} {status_bot if status_bot else _("Отключено")}\n")
        status_cpg = _("Работает") if status_prg else _("Выключено")
        user_status = username_block if len(username_block) else _("Не найдено")
        timer_status = time if time else _("Не включено")
        bot_status = status_bot if status_bot else _("Отключено")

        await update.message.reply_text(
                _("СТАТУС ПРОГРАММЫ:\n- CPG: {status_cpg}\n- Пользователь: {user_status}\n- Таймер: {timer_status}\n"
                  "- Оповещение Telegram: {bot_status}"
                  ).format(
                        status_cpg=status_cpg,
                        user_status=user_status,
                        timer_status=timer_status,
                        bot_status=bot_status
                )
        )

    elif text == _("Разблокировать ПК"):
        await update.message.reply_text(_("Пользователь {username} разблокирован.").format(username=username_block))
    elif text == _("Выключить ПК"):
        os.system("shutdown /s /t 30")  # Выключение ПК с таймером в 30 секунд
        await update.message.reply_text(_("ПК будет выключен через 30 секунд."))

    elif text == _("Выключить приложение"):
        await update.message.reply_text(_("Приложение выключено.\nВсе настройки стерты.\nТаймер остановлен.\n БЛОКИРОВКА НЕ СНЯТА"))

    elif text == _("Включить приложение"):
        await update.message.reply_text(_("Приложение включено."))

    elif text == _("Выбрать время для блокировки"):
        await choose_time(update, context)


# Главная функция запуска приложения бота
async def main_bot_run():
    """Главная функция запуска приложения бота"""
    # ------- Проверка кода ошибки -------
    # Создание мьютекса
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, MUTEX_NAME_BCPG)
    error_code = ctypes.windll.kernel32.GetLastError()

    if error_code == 183:
        os._exit(0)
    elif error_code == 5:  # ERROR_ACCESS_DENIED
        if mutex != 0:  # Проверяем, что дескриптор валиден перед закрытием
            ctypes.windll.kernel32.CloseHandle(mutex)

        function.show_message_with_auto_close(_("Доступ к мьютексу запрещен."), _("ОШИБКА"))
        return
    elif error_code != 0:
        if mutex != 0:  # Проверяем, что дескриптор валиден перед закрытием
            ctypes.windll.kernel32.CloseHandle(mutex)

        error_message = _("Неизвестная ошибка:\n{error_code}").format(error_code=error_code)
        title = _("ОШИБКА")
        function.show_message_with_auto_close(error_message, title)
        return
    # -------------- END ---------------

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
        # Закрытие мьютекса при завершении
        if mutex != 0:
            ctypes.windll.kernel32.CloseHandle(mutex)

        await shutdown(application, mutex)  # Корректное завершение работы бота


# --------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    # Запускаем бота
    asyncio.run(main_bot_run())
