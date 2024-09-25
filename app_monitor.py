import ctypes
import json
import os
import time
import psutil
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

from config_app import path_data_file, DISK_LETTER, path_log_file
from function import run_as_admin

# Путь к .exe файлу, который нужно мониторить
path_to_program = os.path.join(DISK_LETTER, "Program Files (x86)", "Child PC Guard.exe")


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

        current_date = datetime.now().date()

        if current_date > datetime.strptime(data['date'], '%Y-%m-%d').date():
            data['date'] = str(current_date)
            if data['remaining_time'] >= 0:
                data['remaining_time'] += 7200
            data['username_blocking'] = 'test'

            with open(path_data_file, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            print(f"Данные обновлены: {data}")
        else:
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
    log_file_path = path_log_file
    try:
        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            log_file.write(f"MONITOR_CPG({time.strftime('%Y-%m-%d %H:%M:%S')}) -"
                           f" {message}\n==================\n"
                           )
    except Exception as e:
        print(f"Ошибка при записи лога в файл лога: {str(e)}")
        ctypes.windll.user32.MessageBoxW(
                None,
                f"MONITOR_CPG({time.strftime('%Y-%m-%d %H:%M:%S')}) - {message}\n==================\n",
                "Ошибка",
                1
        )


# Основная секция для запуска программы
if __name__ == '__main__':
    # Запуск приложения как администратора
    run_as_admin()

    # Создаем экземпляр планировщика
    scheduler = BlockingScheduler()

    # Задача 1: Следить за процессом и перезапускать, если не запущен (каждые 60 секунд)
    scheduler.add_job(check_and_restart_program, 'interval', seconds=60)

    # Задача 2: Следить за датой и обновлять данные (каждый час)
    scheduler.add_job(update_data, 'interval', hours=1)

    # TODO секундах для теста работы
    # scheduler.add_job(update_data, 'interval', seconds=10)

    try:
        print("Запуск планировщика...")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        # Отключаем планировщик
        scheduler.shutdown()
        print("Планировщик остановлен.")
