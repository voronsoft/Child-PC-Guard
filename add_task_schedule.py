"""
Файл отвечает за автоматизацию процесса добавления задания
(для запуска мониторинга за программой Child PC Guard), в планировщике заданий.
"""

import ctypes
import os
import subprocess
import sys
import time

# Определяем корневую папку проекта
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
# Получаем имя диска (вид С:\)
DISK_LETTER = os.path.splitdrive(PROJECT_ROOT)[0] + "\\"
# TODO Путь к папке с данными
FOLDER_DATA = os.path.join(DISK_LETTER, "ProgramData", "Child PC Guard Data")
# Путь к файлу логов - log_chpcgu.txt
PATH_LOG_FILE = os.path.join(FOLDER_DATA, "log_chpcgu.txt")

# Получаем путь к файлу XML
if getattr(sys, "frozen", False):
    # Если приложение запущено как исполняемый файл (.exe), используем _MEIPASS
    base_path = sys._MEIPASS  # noqa
else:
    # Если приложение запущено из исходного кода (.py), используем текущую директорию
    base_path = os.path.dirname(__file__)

# Указываем путь к XML файлу (относительный путь к файлу XML)
xml_path = os.path.join(base_path, "task_data.xml")


# ---------------------
def set_full_access(directory_path):
    """Устанавливает полный доступ для всех пользователей к указанной папке и её вложениям."""
    try:
        # Выполняем команду icacls для установки полных прав на папку и все вложенные файлы
        command = f'icacls "{directory_path}" /grant Everyone:F /T /C'
        subprocess.run(command, shell=True, check=True)
        print(f"Полный доступ установлен для {directory_path}")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при установке прав доступа:\n{str(e)}")


def create_directory_with_permissions(directory_path):
    """Создаёт папку и устанавливает полный доступ для всех пользователей."""
    try:
        # Создаём папку, если её ещё нет
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            print(f"Папка создана: {directory_path}")
        # Устанавливаем полный доступ
        set_full_access(directory_path)
    except Exception as e:
        print(f"Ошибка при создании папки или установке прав:\n{str(e)}")


def log_error(message):
    """Метод для логирования ошибок в файл."""
    directory_path = os.path.dirname(PATH_LOG_FILE)

    # Проверяем, существует ли папка для логов
    if not os.path.exists(directory_path):
        create_directory_with_permissions(directory_path)

    try:
        # Проверяем, существует ли файл
        mode = "w" if not os.path.exists(PATH_LOG_FILE) else "a"
        with open(PATH_LOG_FILE, mode, encoding="utf-8") as log_file:
            log_file.write(f"ADD_TASK_SCHEDULE({time.strftime('%Y-%m-%d %H:%M:%S')}) - {message}\n==================\n")
        if mode == "w":
            print(f"Лог-файл был создан: {PATH_LOG_FILE}")
    except Exception as e:
        print(f"(add_task_schedule) Ошибка при записи в лог-файл:\n{str(e)}")


# ---------------------


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
            ctypes.windll.shell32.ShellExecuteW(
                None,
                "runas",
                sys.executable,
                " ".join([f'"{arg}"' for arg in sys.argv]),
                None,
                1,  # 1 - отображать консоль; 0 - скрыть консоль
            )
            sys.exit()  # Завершаем текущий процесс, чтобы предотвратить двойной запуск
        except Exception as e:
            log_error(f"Не удалось запустить программу с правами администратора:\n{e}")


def run_powershell_commands():
    """
    Выполняет команды PowerShell для установки политики выполнения, получения пути к XML
    и регистрации задачи в планировщике заданий.
    """
    # Устанавливаем политику выполнения для текущей сессии
    set_policy_command = "Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process"

    # Команда для чтения XML файла и регистрации задачи в планировщике заданий
    register_task_command = f"""
    $xmlContent = Get-Content -Path '{xml_path}' -Raw;
    Register-ScheduledTask -Xml $xmlContent -TaskName 'Start CPG Monitor';
    """

    # Выполняем команды в PowerShell
    try:
        # Выполняем команду для установки политики выполнения
        subprocess.run(["powershell", "-Command", set_policy_command], check=True)

        # Выполняем команду для регистрации задачи через PowerShell
        subprocess.run(["powershell", "-Command", register_task_command], check=True)
        log_error("Задача 'Start CPG Monitor'\nуспешно зарегистрирована в планировщике заданий.")

    except subprocess.CalledProcessError as e:
        log_error(f"Произошла ошибка при выполнении PowerShell команд:\n - {e}")

        sys.exit(1)  # Завершаем программу с кодом ошибки


def check_task_exists(tsk_name):
    """
    Проверяет, существует ли задача в планировщике задач.

    :param tsk_name: Имя задачи для проверки.
    :return: True, если задача существует, иначе False.
    """

    try:
        # Выполняем команду для проверки существования задания
        command = ["schtasks", "/Query", "/TN", tsk_name]
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False


if __name__ == "__main__":
    run_as_admin()  # Проверяем и запускаем от имени администратора

    # Указываем имя задачи для проверки
    task_name = "Start CPG Monitor"
    # Проверяем, существует ли задача
    if check_task_exists(task_name):
        log_error(f"Задача '{task_name}'\nуже существует в планировщике задач. Установка отменена.")

        sys.exit()  # Завершаем выполнение, если задача уже существует
    else:
        run_powershell_commands()  # Выполняем команды PowerShell напрямую из Python

        sys.exit(1)  # Завершаем программу с кодом ошибки
