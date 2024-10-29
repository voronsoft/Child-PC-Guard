"""
Главное приложение мониторинга за программой:
 - Child PC Guard.exe
 - run_bot_telegram.exe
 - Обновляет дату каждый день в файле данных приложения Child PC Guard.exe и добавляет пользователю 2 часа.
"""

import asyncio
import ctypes
import json
import os
import sys
import time
from datetime import datetime

import psutil

import function
from config_app import (PATH_DATA_FILE, PATH_LOG_FILE, path_bot_tg_exe,
                        path_main_app
                        )

# Имя мьютекса (оно должно быть уникальным в системе)
MUTEX_NAME_CPGM = "Global\\CPG_MONITOR"

# Пути к основным приложениям, которые необходимо проверять
path_to_program = path_main_app  # Основное приложение
path_to_program_bot = path_bot_tg_exe  # Telegram-бот

mame_prog_cpg = "Child PC Guard.exe"
name_prog_bot = "run_bot_telegram.exe"


def log_error_monitor(message):
    """
    Логирование ошибок или событий мониторинга в файл.

    :param message: Текст сообщения для записи в лог.
    """
    try:
        # Открываем файл в режиме добавления
        with open(PATH_LOG_FILE, 'a', encoding='utf-8') as log_file:
            # Записываем сообщение с временной меткой
            log_file.write(f"MONITOR_CPG({time.strftime('%Y-%m-%d %H:%M:%S')}) - {message}\n==================\n")
    except Exception as e:
        # Если не удается записать в файл, выводим ошибку в консоль
        print(f"Ошибка при записи лога: {e}")


async def check_and_restart_program():
    """
    Проверяет, запущено ли приложение Child PC Guard.exe.
    Если не запущено, запускает его, если не в защищенной сессии.
    """
    log_error_monitor("Проверка Child PC Guard...")
    # Получаем имя защищенного пользователя из JSON
    usr_protect = function.read_data_json("protected_user")
    # Получаем имя пользователя текущей сессии
    usr_ses = os.getlogin()

    # Проверяем, запущена ли программа через список активных процессов
    if any(proc.name() == mame_prog_cpg for proc in psutil.process_iter()):
        print(f"CPG работает")  # Если работает, ничего не делаем
        log_error_monitor("CPG работает")
    elif usr_protect != usr_ses and usr_protect:
        # Если программа не запущена и это не защищенная сессия, запускаем программу
        print("CPG не запущена. Перезапуск...")
        log_error_monitor(f"CPG не запущена. Перезапуск...\nПуть: {path_to_program}")
        try:
            os.startfile(path_to_program)  # Запуск программы
        except Exception as e:
            # Логируем ошибку, если не удалось запустить
            log_error_monitor(f"Ошибка при запуске CPG:\n{e}")
    elif usr_protect == usr_ses and usr_protect:
        log_error_monitor("Сессия защищена, Запуск CPG не требуется!")

    await asyncio.sleep(1)  # Задержка на 1 секунду для асинхронного выполнения



async def check_and_restart_bot():
    """
    Проверяет, запущено ли приложение run_bot_telegram.exe.
    Если не запущено, запускает его.
    """
    log_error_monitor("Проверка run_bot_telegram...")
    if any(proc.name() == name_prog_bot for proc in psutil.process_iter()):
        log_error_monitor("BOT работает")  # Если бот запущен, ничего не делаем
    else:
        # Если бот не запущен, запускаем его
        print("БОТ не запущен. Перезапуск...")
        log_error_monitor(f"БОТ программа не запущена. Перезапуск...\nПуть: {path_to_program_bot}")
        try:
            os.startfile(path_to_program_bot)  # Запуск программы
        except Exception as e:
            # Логируем ошибку при запуске
            log_error_monitor(f"Ошибка при запуске БОТа: {e}\n{(path_to_program_bot)}")
    await asyncio.sleep(1)  # Задержка на 1 секунду


async def update_data():
    """
    Проверяет и обновляет данные в файле JSON. Если текущая дата больше даты в файле:
    - обновляет дату,
    - добавляет 7200 секунд к оставшемуся времени (remaining_time),
    - обновляет имя пользователя (username_blocking).
    """
    try:
        # Открываем файл JSON для чтения
        with open(PATH_DATA_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)  # Загружаем данные в словарь

        current_date = datetime.now().date()  # Получаем текущую дату

        # Если текущая дата больше даты в файле, обновляем данные
        if current_date > datetime.strptime(data['date'], '%Y-%m-%d').date():
            data['date'] = str(current_date)  # Обновляем дату на текущую
            data['remaining_time'] += 7200  # Добавляем 7200 секунд к оставшемуся времени

            usr_ses = os.getlogin()  # Получаем имя пользователя текущей сессии
            print("========== ", usr_ses)
            if not data['username_blocking']:
                # Если поле 'username_blocking' пустое, записываем имя текущего пользователя
                data['username_blocking'] = usr_ses

            if data['username_blocking'] == function.read_data_json("protected_user"):
                # Если имя совпадает с защищенным пользователем, очищаем блокировку
                data['username_blocking'] = ""
                data['remaining_time'] = 0  # Обнуляем оставшееся время

            # Открываем файл для записи обновленных данных
            with open(PATH_DATA_FILE, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)  # Записываем обновленные данные

            log_error_monitor(f"Данные обновлены: {data}")  # Логируем обновление данных
        else:
            # Если текущая дата не больше, логируем, что обновление не нужно
            log_error_monitor("Дата не обновлена, текущая дата не больше даты из файла.")
    except Exception as e:
        # Логируем ошибку при попытке обновить данные
        log_error_monitor(f"Ошибка обновления данных даты: {e}")
    await asyncio.sleep(1)  # Задержка на 1 секунду


async def main_monitor():
    """
    Основная функция мониторинга. Выполняет:
    - создание мьютекса для предотвращения повторного запуска программы,
    - запуск всех проверок асинхронно.
    """
    # ------- Проверка кода ошибки -------
    # Создаем, мьютекс (гарантирует, что программа запущена только один раз).
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, MUTEX_NAME_CPGM)
    # Получаем код ошибки
    error_code = ctypes.windll.kernel32.GetLastError()

    function.process_mutex_error(error_code, mutex)
    # -------------- END ---------------

    # Асинхронно запускаем все задачи: проверку программ и обновление данных
    await asyncio.gather(
            check_and_restart_program(),
            check_and_restart_bot(),
            update_data()
    )

    # Освобождаем мьютекс, завершая работу программы
    ctypes.windll.kernel32.ReleaseMutex(mutex)

    sys.exit()


if __name__ == '__main__':
    asyncio.run(main_monitor())  # Запуск основной функции мониторинга
