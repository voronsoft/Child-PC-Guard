import asyncio
import ctypes
import logging
import os
import subprocess
import sys

from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import (Application, CommandHandler, ContextTypes,
                          MessageHandler, filters
                          )

import config_localization
import function

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
    sys.exit()  # 0 обозначает успешное завершение


# Запуск бота
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запуск бота"""
    chat_id = update.message.chat.id

    # Если в БД нет номера chat_id или номера не совпадают выводим сообщение
    if function.read_data_json("chat_id") != chat_id:
        await update.message.reply_text(_("Ваш chat_id: {chat_id}\nЭтот номер вам нужно ввести в программе - Child PC Guard\n"
                                          "Нажав на кнопку в меню - 'Подключить оповещения через - Telegram'\n"
                                          "Введите номер в поле для ввода и нажмите - ОК\n"
                                          "После этого программа сможет понять кому отправлять сообщения"
                                          ).format(chat_id=chat_id)
                                        )
    if function.read_data_json("chat_id") == chat_id:
        await update.message.reply_text(_("Chat_id: {chat_id}").format(chat_id=chat_id))

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
        answer = function.update_data_json("chat_id", chat_id)
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
            [KeyboardButton(_("Выключить и заблокировать ПК"))]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    await update.message.reply_text(_("Меню:"), reply_markup=reply_markup)


# Обработка сообщения с предупреждением
async def handle_warning_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка ввода текста для предупреждения."""
    # Получаем текст сообщения от пользователя
    text = update.message.text

    # Вывод устрашающего предупреждения на экран
    function.show_message_with_auto_close(message=text, delay=30)
    await update.message.reply_text(_("Устрашающее сообщение выведено на главном экране."))


# Обработка сообщений от пользователя.
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка сообщений от пользователя."""
    text = update.message.text
    chat_id = update.message.chat.id
    # ------------------------------
    time_bd = function.read_data_json("remaining_time")
    time = function.seconds_to_hms(time_bd)

    status_prg = function.check_if_program_running("Child PC Guard.exe")

    status_bot = function.read_data_json("chat_id")

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
        # ---- Имя пользователя для кого назначена блокировка. ----
        # Получаем имя пользователя из БД
        username_block_bd = function.read_data_json("username_blocking")
        # Получаем имя пользователя из системы windows если есть заблокированные учетные записи
        username_block_sistem = function.get_block_user()

        # Выбираем имя пользователя исходя из значения из БД или данных из системы
        # Если имя в БД не пустое
        if len(username_block_bd) >= 2:
            username_block = username_block_bd
        # Если найден в системе заблокированный пользователь
        elif len(username_block_sistem) >= 2 and len(username_block_bd) == 0:
            username_block = username_block_sistem
        else:
            username_block = _("Не найдено")

        # статус программы
        status_cpg = _("Работает") if status_prg else _("Выключено")
        # имя пользователя
        user_status = username_block
        # время таймера
        timer_status = time if time != "00:00:00" else _("Не включено")
        # статус бота
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

    elif text == _("Выключить и заблокировать ПК"):
        # Выводим имена пользователей из системы
        usr_act_ses = function.username_session()
        await update.message.reply_text(
                _("Имя пользователя который будет заблокирован:\n{usr_act_ses}").format(usr_act_ses=usr_act_ses)
        )
        # Запрашиваем имя блокируемого пользователя
        await update.message.reply_text(_("Введите это имя для подтверждения блокировки и выключения ПК:"))
        context.user_data['waiting_for_username'] = True

    elif context.user_data.get('waiting_for_username'):
        # Получаем введенное имя пользователя
        username = text.strip()
        # Получаем имя защищенного пользователя
        protect_usr = function.read_data_json("protected_user")
        # Получаем имя пользователя активной сессии
        session_usr = function.username_session()

        # Если имя не совпадает с именем защищенного пользователя
        # и имя совпадает с именем пользователя активной сессии
        if protect_usr != username and username == session_usr:
            # Если имя введено, блокируем пользователя
            command_disable_user = f'net user "{username}" /active:no'
            subprocess.run(command_disable_user, shell=True, check=True)
            await update.message.reply_text(
                    _("Пользователь {username} будет заблокирован. ПК будет выключен через 30 секунд.").format(username=username)
            )
            # Выключение ПК
            os.system("shutdown /s /t 30")
            context.user_data['waiting_for_username'] = False
        elif protect_usr == username:
            # Если имя совпадает с именем защищенного пользователя
            await update.message.reply_text(_("Этот пользователь защищен от блокировки. Отмена операции."))
        elif username != session_usr:
            # Если имя не совпадает с именем активной сессии
            await update.message.reply_text(_("Имя пользователя указано неверно. Отмена операции."))





# Главная функция запуска приложения бота
async def main_bot_run():
    """Главная функция запуска приложения бота"""
    # ------- Проверка кода ошибки -------
    # Создание мьютекса
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, MUTEX_NAME_BCPG)
    error_code = ctypes.windll.kernel32.GetLastError()

    function.process_mutex_error(error_code, mutex)
    # -------------- END ---------------

    # Создаем приложение Telegram
    application = Application.builder().token(TOKEN).build()

    # Команда /start для запуска меню
    application.add_handler(CommandHandler("start", start))

    # Обработчик для проверки пароля
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_password))

    try:
        # Запуск бота
        await application.initialize()  # Инициализация приложения
        await application.start()
        await application.updater.start_polling()
        # Ждем сигнала для завершения работы
        # Это основной цикл, который ждет завершения
        await asyncio.Event().wait()

    except (KeyboardInterrupt, SystemExit):
        print(1)
        # Закрытие мьютекса при завершении
        await shutdown(application, mutex)  # Корректное завершение работы бота
    except Exception as e:
        print(2)
        # Закрытие мьютекса при завершении
        if mutex != 0:
            ctypes.windll.kernel32.CloseHandle(mutex)

        sys.exit()  # 0 обозначает успешное завершение


# --------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    # Запускаем бота
    asyncio.run(main_bot_run())
