# Главное приложение мониторинга за программой - Child PC Guard.exe
# Следит за запуском и перезапускает приложение если оно было закрыто.
# Обновляет дату каждый день в файле данных приложения Child PC Guard.exe и добавляет пользователю 2 часа.
import os
import sys
import json
import time
import psutil
import ctypes
import win32con
import subprocess
import win32process
import win32security
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

# Имя мьютекса (должно быть уникальным)
MUTEX_NAME = "Global\\Child_PC_Monitor"

# ----------------- Основные переменные. ------------------------
# Определяем корневую папку проекта.
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
# Получаем имя диска (вид С:\)
DISK_LETTER = os.path.splitdrive(PROJECT_ROOT)[0] + "\\"
# Путь к папке с данными
FOLDER_DATA = os.path.join(DISK_LETTER, "ProgramData", "Child PC Guard Data")
PATH_APP = os.path.join(DISK_LETTER, "Program Files (x86)", "Child PC Guard", "Child PC Guard.exe")

# Путь к .exe файлу, который нужно мониторить
path_to_program = PATH_APP
# Путь к файлу данных - data.json
path_data_file = os.path.join(FOLDER_DATA, "data.json")
# Путь к файлу логов - log_chpcgu.txt
path_log_file = os.path.join(FOLDER_DATA, "log_chpcgu.txt")

# ---------------------------- END ------------------------------
def is_admin():
    """Проверяет, запущен ли скрипт с правами администратора."""
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def run_as_admin():
    """Запускает приложение с правами администратора, если это не так."""
    if not is_admin():
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

            if response <= 32:
                print(f"Не удалось запросить права администратора. Код ошибки: {response}")
                log_error_monitor(f"Не удалось запросить права администратора. Код ошибки: {response}")
                ctypes.windll.user32.MessageBoxW(
                    None,
                    f"Не удалось запустить программу с правами администратора. Код ошибки: {response}",
                    "Ошибка",
                    0
                )
                sys.exit()  # Выход из программы при ошибке
            else:
                sys.exit()  # Завершаем текущий процесс, чтобы предотвратить двойной запуск
        except Exception as e:
            print(f"Не удалось запустить программу с правами администратора:\n{e}")
            log_error_monitor(f"Не удалось запросить права администратора:\n{e}")
            ctypes.windll.user32.MessageBoxW(
                None,
                f"Не удалось запустить программу с правами администратора:\n\n{e}",
                "Ошибка",
                0
            )
            sys.exit()  # Выход из программы при ошибке


def run_in_user_session(program_path):
    """Запуск приложения в контексте пользовательской сессии"""
    # Получаем дескриптор текущего активного пользователя
    token = None
    session_id = None
    for session in psutil.users():
        if session.terminal == 'console':  # Убедимся, что это активная пользовательская сессия
            session_id = session.name
            break

    if session_id is None:
        print("!!!- Пользовательская сессия не найдена.")
        log_error_monitor("!!!- Пользовательская сессия не найдена.")
        return False

    # Получаем дескриптор пользователя
    token_handle = win32security.LogonUser(
            session_id, None, None, win32con.LOGON32_LOGON_INTERACTIVE, win32con.LOGON32_PROVIDER_DEFAULT
    )

    # Запуск процесса в пользовательской сессии
    if token_handle:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = win32con.SW_SHOW  # Отобразить окно приложения

        process_info = win32process.CreateProcessAsUser(
                token_handle,  # Токен пользователя
                None,  # Путь к приложению
                program_path,  # Команда
                None,  # Дескриптор безопасности
                None,  # Дескриптор безопасности
                False,  # Наследовать дескрипторы
                0,  # Флаги
                None,  # Переменные среды
                None,  # Рабочая директория
                startupinfo  # Информация о старте
        )
        print(f"Приложение запущено в пользовательской сессии. PID: {process_info[2]}")
        log_error_monitor(f"Приложение запущено в пользовательской сессии. PID: {process_info[2]}")
        return True
    else:
        print("!!!- Не удалось получить токен пользовательской сессии, для запуска приложения в контексте "
              "пользовательской сессии")
        log_error_monitor("!!!- Не удалось получить токен пользовательской сессии, для запуска приложения в контексте "
              "пользовательской сессии")
        return False


def check_and_restart_program():
    """Проверяет, запущена ли программа, и перезапускает ее, если она не запущена."""
    program_running = False
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'Child PC Guard.exe':
            program_running = True
            break

    if not program_running:
        print("Программа Child PC Guard не запущена. Перезапуск...")
        log_error_monitor("Программа Child PC Guard не запущена. Перезапуск...")

        try:
            if os.path.exists(path_to_program):
                # Запуск приложения в контексте пользовательской сессии
                # os.startfile(path_to_program)  # Простой запуск без учета сессии
                run_in_user_session(path_to_program)  # Используем запуск в пользовательской сессии
            else:
                log_error_monitor(f"(1) Программа Child PC Guard.exe не найдена по пути\n{path_to_program}")
                return True  # Возвращаем True, чтобы указать, что планировщик нужно остановить
        except Exception as e:
            print(f"Не удалось запустить Блокировщик:\n{e}")
            log_error_monitor(f"Не удалось запустить Блокировщик:\n{e}")
            return True  # Возвращаем True, чтобы указать, что планировщик нужно остановить
    return False  # Возвращаем False, если программа запущена


def update_data():
    """Обновляет данные в файле."""
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
        return True  # Возвращаем True, чтобы указать, что планировщик нужно остановить
    except json.JSONDecodeError:
        print("Планировщик остановлен. Ошибка чтения JSON из файла.")
        log_error_monitor("Планировщик остановлен. Ошибка чтения JSON из файла.")
        return True  # Возвращаем True, чтобы указать, что планировщик нужно остановить
    except Exception as e:
        print(f"Планировщик остановлен. Ошибка:\n{e}")
        log_error_monitor(f"Планировщик остановлен.:\n{e}")
        return True  # Возвращаем True, чтобы указать, что планировщик нужно остановить
    return False  # Возвращаем False, если ошибок не было


def log_error_monitor(message):
    """Метод для логирования ошибок в файл."""
    try:
        with open(path_log_file, 'a', encoding='utf-8') as log_file:
            log_file.write(f"MONITOR_CPG({time.strftime('%Y-%m-%d %H:%M:%S')}) - {message}\n==================\n")
    except Exception as e:
        print(f"Ошибка при записи лога в файл лога: {str(e)}")
        ctypes.windll.user32.MessageBoxW(
            None,
            f"MONITOR_CPG({time.strftime('%Y-%m-%d %H:%M:%S')}) - {message}\n==================\n",
            "Ошибка",
            0
        )

def main():
    # ------- Проверка кода ошибки -------
    # Создание мьютекса
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, MUTEX_NAME)
    error_code = ctypes.windll.kernel32.GetLastError()

    if error_code == 183 or error_code == 5:
        ctypes.windll.user32.MessageBoxW(None, f"Приложение Child PC Monitor уже запущено.", "ПРЕДУПРЕЖДЕНИЕ", 0)
        # Закрываем дескриптор мьютекса, так как он не нужен
        ctypes.windll.kernel32.CloseHandle(mutex)
        return
    elif error_code != 0:
        ctypes.windll.user32.MessageBoxW(None, f"Неизвестная ошибка:\n{error_code}", "ОШИБКА", 0)
        # Закрываем дескриптор мьютекса
        ctypes.windll.kernel32.CloseHandle(mutex)
        return
    # -------------- END ---------------

    run_as_admin()

    # Проверка на наличие программы при старте
    if not os.path.exists(path_to_program):
        print("Программа Child PC Guard не найдена по указанному пути. Планировщик будет остановлен")
        log_error_monitor("Программа Child PC Guard не найдена по указанному пути. Планировщик будет остановлен")
        sys.exit()  # Завершаем выполнение, если программа не найдена

    # Создаем экземпляр планировщика
    scheduler = BlockingScheduler()

    # Задача 1: Следить за процессом и перезапускать, если не запущен (каждые 10 секунд)
    scheduler.add_job(check_and_restart_program, 'interval', seconds=10)

    # Задача 2: Следить за датой и обновлять данные (каждые 10 секунд)
    scheduler.add_job(update_data, 'interval', seconds=10)

    try:
        print("Запуск планировщика...")
        while True:
            # Проверяем, нужно ли остановить планировщик
            if check_and_restart_program() or update_data():
                print("Остановка планировщика из-за ошибок.")
                log_error_monitor("Остановка планировщика из-за ошибок.")
                break  # Прерываем цикл, если необходимо завершить работу
            time.sleep(10)  # Задержка между итерациями
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("Планировщик остановлен.")
    finally:
        scheduler.shutdown()


# Основная секция для запуска программы
if __name__ == '__main__':
    main()
