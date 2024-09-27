import ctypes
import json
import os
import sys
import time
import psutil
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

# ----------------- Основные переменные. ------------------------
# Определяем корневую папку проекта.
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
# Получаем имя диска (вид С:\)
DISK_LETTER = os.path.splitdrive(PROJECT_ROOT)[0] + "\\"
# Путь к папке с данными
FOLDER_DATA = os.path.join(DISK_LETTER, "ProgramData", "Child PC Guard Data")

# Путь к .exe файлу, который нужно мониторить
path_to_program = os.path.join(DISK_LETTER, "Program Files (x86)", "Child PC Guard.exe")
# Путь к файлу данных - data.json
path_data_file = os.path.join(FOLDER_DATA, "data.json")
# Путь к файлу логов - log_chpcgu.txt
path_log_file = os.path.join(FOLDER_DATA, "log_chpcgu.txt")


# ---------------------------- END ------------------------------
def is_admin():
    """
    Проверяет, запущен ли скрипт с правами администратора.

    :return: True, если запущен с правами администратора, иначе False.
    """
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def run_as_admin():
    """
    Проверяет, запущено ли приложение с правами администратора.
    Если нет, перезапускает его с запросом прав администратора.
    """
    if not is_admin():
        # Перезапускаем с запросом прав администратора
        try:
            print("Запрос прав администратора...")
            response = ctypes.windll.shell32.ShellExecuteW(
                    None,
                    "runas",
                    sys.executable,
                    ' '.join([f'"{arg}"' for arg in sys.argv]),
                    None,
                    1  # 1-отобразить консоль \ 0-скрыть консоль
            )

            # Проверяем, удалось ли запустить программу с правами администратора
            if response <= 32:
                print(f"Не удалось запросить права администратора. Код ошибки: {response}")
                ctypes.windll.user32.MessageBoxW(
                        None,
                        f"Не удалось запустить программу с правами администратора. Код ошибки: {response}",
                        "Ошибка",
                        0
                )
            else:
                sys.exit()  # Завершаем текущий процесс, чтобы предотвратить двойной запуск
        except Exception as e:
            print(f"Не удалось запустить программу с правами администратора:\n{e}")
            ctypes.windll.user32.MessageBoxW(
                    None,
                    f"Не удалось запустить программу с правами администратора:\n\n{e}",
                    "Ошибка",
                    0
            )


# Функция для проверки, запущена ли программа
def check_and_restart_program():
    program_running = False
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'Child PC Guard.exe':  # Убедитесь, что имя программы правильное
            program_running = True
            break

    if not program_running:
        print("Программа Child PC Guard не запущена. Перезапуск...")
        # Сообщение записываем в log
        log_error_monitor(f"Программа Child PC Guard не запущена. Перезапуск...")

        try:
            # os.startfile(path_to_program)  # Перезапуск программы
            ...
        except Exception as e:
            print(f"Планировщик остановлен. Не удалось запустить Блокировщик:\n{e}")
            # Отключаем планировщик
            log_error_monitor(f"Планировщик остановлен. Не удалось запустить Блокировщик:\n{e}")
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

            print(f"Дата обновлена в файле данных: {data}")
            log_error_monitor(f"Дата обновлена в файле данных: {data}")
        else:
            print("Дата не обновлена, реальная дата не больше даты из файла.")


    except FileNotFoundError:
        print("Планировщик остановлен, файл data.json не найден.")
        log_error_monitor("Планировщик остановлен, файл data.json не найден.")
        scheduler.shutdown()
    except json.JSONDecodeError:
        print("Планировщик остановлен. Ошибка чтения JSON из файла.")
        log_error_monitor("Планировщик остановлен. Ошибка чтения JSON из файла.")
        scheduler.shutdown()
    except Exception as e:
        print(f"Планировщик остановлен. Ошибка:\n{e}")
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
        ctypes.windll.user32.MessageBoxW(
                None,
                f"MONITOR_CPG({time.strftime('%Y-%m-%d %H:%M:%S')}) - {message}\n==================\n",
                "Ошибка",
                0
        )


# Основная секция для запуска программы
if __name__ == '__main__':
    # Добавим лог перед проверкой на администратора
    print("Проверка прав администратора...")

    # Запуск приложения как администратора
    # run_as_admin()

    # Если программа дошла до этого момента, значит она запущена с нужными правами
    print("Программа запущена с правами администратора.")

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
