# Главное приложение мониторинга за программой - Child PC Guard.exe
# Следит за запуском и перезапускает приложения если оно было закрыто.
# Обновляет дату каждый день в файле данных приложения Child PC Guard.exe и добавляет пользователю 2 часа.

import os
import json
import time
import ctypes
from pprint import pprint

import psutil
import traceback
import config_localization
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from config_app import PATH_DATA_FILE, PATH_LOG_FILE, path_main_app, path_bot_tg_exe
from function import run_as_admin, show_message_with_auto_close, send_bot_telegram_message, read_data_json

# Подключаем локализацию
_ = config_localization.setup_locale(read_data_json("language"))

# Имя мьютекса (должно быть уникальным)
MUTEX_NAME_CPGM = "Global\\CPG_MONITOR"
# TODO Путь к .exe файлу, который нужно мониторить
path_to_program = path_main_app
path_to_program_bot = path_bot_tg_exe


# Функция для проверки, запущена ли программа
def check_and_restart_program():
    print("\nПроверка программ...")  # Отладочный принт
    program_running = False
    bot_program_running = False

    # Получаем список всех запущенных процессов в ос
    proc_run_os = [proc.info['name'] for proc in psutil.process_iter(['pid', 'name'])]

    # Проверяем, запущены ли приложения
    if "Child PC Guard.exe" in proc_run_os:  # Приложение - CPG
        program_running = True

    if "run_bot_telegram.exe" in proc_run_os:  # Приложение - BOT
        bot_program_running = True

    # Главная программа запуск
    if not program_running:
        print("CPG не запущена. Перезапуск...")
        # Сообщение записываем в log
        log_error_monitor(f"CPG не запущена. Перезапуск...\nПуть: {path_to_program}")
        try:
            # Запускаем .exe файл через subprocess
            os.startfile(path_to_program)
        except Exception as e:
            print("1 Планировщик остановлен.")
            send_bot_telegram_message(_("1 MonitorCPG - Планировщик остановлен."))
            # Отключаем планировщик
            log_error_monitor(f"1 MonitorCPG - Планировщик остановлен.:\n{e}")
            scheduler.shutdown(wait=False)
    else:
        print("CPG работает")

    # Задаем паузу 5ть секунд
    time.sleep(5)
    # -------- END ----------

    # Бот программа запуск
    if not bot_program_running:
        print("БОТ программа не запущена. Перезапуск...")
        # Сообщение записываем в log
        log_error_monitor(f"БОТ программа не запущена. Перезапуск...\nПуть: {path_to_program_bot}")

        try:
            # Запускаем .exe файл через subprocess
            os.startfile(path_to_program_bot)
        except Exception as e:
            print("1-1 Планировщик остановлен.")
            send_bot_telegram_message(_("1-1 MonitorCPG - Планировщик остановлен."))

            # Отключаем планировщик
            log_error_monitor(f"1-1 MonitorCPG - Планировщик остановлен.:\n{e}")
            scheduler.shutdown(wait=False)
    else:
        print("BOT работает")


# Функция для обновления данных в файле
def update_data():
    try:
        with open(PATH_DATA_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)

        current_date = datetime.now().date()  # Получаем дату нынешнего дня

        if current_date > datetime.strptime(data['date'], '%Y-%m-%d').date():
            data['date'] = str(current_date)
            if data['remaining_time'] >= 0:
                data['remaining_time'] += 7200
            # TODO имя пользователя получаем из активной сессии
            username = os.getlogin()  # Получаем имя пользователя сессии в которой запущена программа
            data['username_blocking'] = f'{username}'  # Записываем в файл имя пользователя для блокировки

            with open(PATH_DATA_FILE, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            print(f"Данные обновлены: {data}")
            log_error_monitor(f"Данные обновлены: {data}")
        else:
            log_error_monitor("Дата не обновлена, реальная дата не больше даты из файла.")
            print("Дата не обновлена, реальная дата не больше даты из файла.")

    except FileNotFoundError:
        print("2 Файл data.json не найден. Планировщик остановлен.")
        send_bot_telegram_message(_("2 Файл data.json не найден. Планировщик остановлен."))
        log_error_monitor("2 Файл data.json не найден. Планировщик остановлен.")
        scheduler.shutdown(wait=False)
    except json.JSONDecodeError:
        print("3 Ошибка чтения JSON из файла. Планировщик остановлен.")
        log_error_monitor("3 Ошибка чтения JSON из файла. Планировщик остановлен.")
        scheduler.shutdown(wait=False)
    except Exception as e:
        print("4 Планировщик остановлен.")
        send_bot_telegram_message(_("4 Планировщик остановлен."))
        # Отключаем планировщик
        log_error_monitor(f"4 Планировщик остановлен.:\n{e}")
        scheduler.shutdown(wait=False)


def log_error_monitor(message):
    """Метод для логирования ошибок в файл."""
    try:
        with open(PATH_LOG_FILE, 'a', encoding='utf-8') as log_file:
            log_file.write(f"MONITOR_CPG({time.strftime('%Y-%m-%d %H:%M:%S')}) -"
                           f" {message}\n==================\n"
                           )
    except Exception as e:
        print(f"Ошибка при записи лога в файл лога: {str(e)}")
        show_message_with_auto_close(
                f"MONITOR_CPG({time.strftime('%Y-%m-%d %H:%M:%S')}) - {message}\n==================\n",
                "Ошибка"
        )


def main_run_monitor():
    global scheduler
    # Запуск приложения как администратора
    run_as_admin()

    # ------- Проверка кода ошибки -------
    # Создание мьютекса
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, MUTEX_NAME_CPGM)
    error_code = ctypes.windll.kernel32.GetLastError()

    if error_code == 183:
        print(183)
        return
    elif error_code == 5:  # ERROR_ACCESS_DENIED
        if mutex != 0:  # Проверяем, что дескриптор валиден перед закрытием
            ctypes.windll.kernel32.CloseHandle(mutex)
        show_message_with_auto_close("MonitorCPG - Доступ к мьютексу запрещен.", "ОШИБКА")
        return
    elif error_code != 0:
        if mutex != 0:  # Проверяем, что дескриптор валиден перед закрытием
            ctypes.windll.kernel32.CloseHandle(mutex)
        show_message_with_auto_close(f"MonitorCPG - Неизвестная ошибка:\n{error_code}", "ОШИБКА")
        return
    # -------------- END ---------------

    # Создаем экземпляр планировщика
    scheduler = BlockingScheduler()

    # TODO Настройка времени для заданий в мониторинге (релиз\разработка)
    # Задача 1: Следить за процессом и перезапускать, если не запущен (каждые 60 секунд)
    scheduler.add_job(check_and_restart_program, 'interval', seconds=60)  # TODO Включить в момент релиза
    # scheduler.add_job(check_and_restart_program, 'interval', seconds=10)  # Отключить после разработки

    # Задача 2: Следить за датой и обновлять данные (каждый 1 час)
    # scheduler.add_job(update_data, 'interval', hours=1)  # TODO Включить в момент релиза
    scheduler.add_job(update_data, 'interval', seconds=10)  # Отключить после разработки

    try:
        print("Запуск заданий")
        scheduler.start()

    except Exception as e:
        log_error_monitor(f"MonitorCPG - Ошибка в главном цикле планировщика: {str(e)}\n{traceback.format_exc()}")
        if scheduler.running:
            scheduler.shutdown(wait=False)

    except (KeyboardInterrupt, SystemExit):
        print("5 Планировщик остановлен.")
        send_bot_telegram_message(_("5 MonitorCPG - Планировщик остановлен."))
        # Отключаем планировщик
        scheduler.shutdown()

if __name__ == '__main__':
    main_run_monitor()
