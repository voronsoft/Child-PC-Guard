# Главное приложение мониторинга за программой - Child PC Guard.exe
# Следит за запуском и перезапускает приложения если оно было закрыто.
# Обновляет дату каждый день в файле данных приложения Child PC Guard.exe и добавляет пользователю 2 часа.

import json
import os
import time
import ctypes
import psutil
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from config_app import path_data_file, DISK_LETTER, path_log_file
from function import run_as_admin, show_message_with_auto_close

# Имя мьютекса (должно быть уникальным)
MUTEX_NAME = "Global\\CPG_MONITOR"
# Путь к .exe файлу, который нужно мониторить
path_to_program = os.path.join(DISK_LETTER, "Program Files (x86)", "Child PC Guard", "Child PC Guard.exe")


# Функция для проверки, запущена ли программа
def check_and_restart_program():
    program_running = False
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'Child PC Guard.exe':  # Убедитесь, что имя программы правильное
            program_running = True
            break

    if not program_running:
        print("Программа не запущена. Перезапуск...")
        # Сообщение записываем в log
        log_error_monitor(f"Программа не запущена. Перезапуск...")

        try:

            os.startfile(path_to_program)  # Перезапуск программы

        except Exception as e:
            print("Планировщик остановлен.")
            # Отключаем планировщик
            log_error_monitor(f"Планировщик остановлен.:\n{e}")
            scheduler.shutdown()


# Функция для обновления данных в файле
def update_data():
    try:
        with open(path_data_file, 'r', encoding='utf-8') as file:
            data = json.load(file)

        current_date = datetime.now().date()  # Получаем дату нынешнего дня

        if current_date > datetime.strptime(data['date'], '%Y-%m-%d').date():
            data['date'] = str(current_date)
            if data['remaining_time'] >= 0:
                data['remaining_time'] += 7200
            # TODO имя пользователя получаем из активной сессии
            username = os.getlogin()  # Получаем имя пользователя сессии в которой запущена программа
            data['username_blocking'] = f'{username}'  # Записываем в файл имя пользователя для блокировки

            with open(path_data_file, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            print(f"Данные обновлены: {data}")
            log_error_monitor(f"Данные обновлены: {data}")
        else:
            log_error_monitor("Дата не обновлена, реальная дата не больше даты из файла.")
            print("Дата не обновлена, реальная дата не больше даты из файла.")

    except FileNotFoundError:
        print("Планировщик остановлен.")
        print("Файл data.json не найден.")
        log_error_monitor("Файл data.json не найден.")
        scheduler.shutdown()
    except json.JSONDecodeError:
        print("Планировщик остановлен.")
        print("Ошибка чтения JSON из файла.")
        log_error_monitor("Ошибка чтения JSON из файла.")
        scheduler.shutdown()
    except Exception as e:
        print("Планировщик остановлен.")
        # Отключаем планировщик
        log_error_monitor(f"Планировщик остановлен.:\n{e}")
        scheduler.shutdown()


def log_error_monitor(message):
    """Метод для логирования ошибок в файл."""
    try:
        with open(path_log_file, 'a', encoding='utf-8') as log_file:
            log_file.write(f"MONITOR_CPG({time.strftime('%Y-%m-%d %H:%M:%S')}) -"
                           f" {message}\n==================\n"
                           )
    except Exception as e:
        print(f"Ошибка при записи лога в файл лога: {str(e)}")
        show_message_with_auto_close(
                f"MONITOR_CPG({time.strftime('%Y-%m-%d %H:%M:%S')}) - {message}\n==================\n",
                "Ошибка"
        )


def main():
    global scheduler
    # Запуск приложения как администратора
    run_as_admin()

    # ------- Проверка кода ошибки -------
    # Создание мьютекса
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, MUTEX_NAME)
    error_code = ctypes.windll.kernel32.GetLastError()

    if error_code == 183:
        # show_message_with_auto_close(f"Приложение Windows CPG MONITOR уже запущено.", "ПРЕДУПРЕЖДЕНИЕ")
        return
    elif error_code == 5:  # ERROR_ACCESS_DENIED
        if mutex != 0:  # Проверяем, что дескриптор валиден перед закрытием
            ctypes.windll.kernel32.CloseHandle(mutex)
        show_message_with_auto_close("Доступ к мьютексу запрещен.", "ОШИБКА")
        return
    elif error_code != 0:
        if mutex != 0:  # Проверяем, что дескриптор валиден перед закрытием
            ctypes.windll.kernel32.CloseHandle(mutex)
        show_message_with_auto_close(f"Неизвестная ошибка:\n{error_code}", "ОШИБКА")

        return
    # -------------- END ---------------

    # Создаем экземпляр планировщика
    scheduler = BlockingScheduler()

    # TODO Настройка времени для заданий в мониторинге
    # Задача 1: Следить за процессом и перезапускать, если не запущен (каждые 60 секунд)
    scheduler.add_job(check_and_restart_program, 'interval', seconds=10)

    # Задача 2: Следить за датой и обновлять данные (каждый час)
    # scheduler.add_job(update_data, 'interval', hours=1)
    scheduler.add_job(update_data, 'interval', seconds=10)

    try:
        print("Запуск планировщика...")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        # Отключаем планировщик
        scheduler.shutdown()
        print("Планировщик остановлен.")

    # Основная секция для запуска программы


if __name__ == '__main__':
    main()
