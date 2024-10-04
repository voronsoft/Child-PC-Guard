# Файл отвечает за автоматизацию процесса добавления задания (для запуска мониторинга за программой Child PC Guard),
# в планировщике заданий.
#
import os
import sys
import time
import ctypes
import subprocess
from function import show_message_with_auto_close

# Определяем корневую папку проекта
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
# Получаем имя диска (вид С:\)
DISK_LETTER = os.path.splitdrive(PROJECT_ROOT)[0] + "\\"
# TODO Путь к папке с данными
FOLDER_DATA = os.path.join(DISK_LETTER, "ProgramData", "Child PC Guard Data")
# Путь к файлу логов - log_chpcgu.txt
PATH_LOG_FILE = os.path.join(FOLDER_DATA, "log_chpcgu.txt")

# Получаем путь к файлу XML
if getattr(sys, 'frozen', False):
    # Если приложение запущено как исполняемый файл, используем _MEIPASS
    base_path = sys._MEIPASS  # noqa

else:
    # Если приложение запущено из исходного кода, используем текущую директорию
    base_path = os.path.dirname(__file__)
# Указываем путь к XML файлу (относительный путь к файлу XML)
xml_path = os.path.join(base_path, "task_data.xml")

print("путь к XML файлу: ", xml_path)


# --------------------------------------------------- XML -------------------------------------------------------------

# -------------------------------------------------END XML ------------------------------------------------------------


# ---------------------
def log_error(message):
    """Метод для логирования ошибок в файл."""
    try:
        with open(PATH_LOG_FILE, 'a', encoding='utf-8') as log_file:
            log_file.write(f"ADD_TASK_SCHEDULE({time.strftime('%Y-%m-%d %H:%M:%S')}) -"
                           f" {message}\n==================\n"
                           )
    except Exception as e:
        show_message_with_auto_close(f"Ошибка при записи лога в файл:\n{str(e)}", "Ошибка")


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
                    ' '.join([f'"{arg}"' for arg in sys.argv]),
                    None,
                    1  # 1 - отображать консоль; 0 - скрыть консоль
            )
            sys.exit()  # Завершаем текущий процесс, чтобы предотвратить двойной запуск
        except Exception as e:
            log_error(f"Не удалось запустить программу с правами администратора:\n{e}")
            show_message_with_auto_close(
                    f"Не удалось запустить программу с правами администратора:\n\n{e}",
                    "Ошибка"
            )


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

        show_message_with_auto_close(
                f"Задача 'Start CPG Monitor'\nуспешно зарегистрирована в планировщике заданий.",
                "Успешно"
        )

    except subprocess.CalledProcessError as e:
        show_message_with_auto_close(
                f"Произошла ошибка при выполнении PowerShell команд:\n - {e}",
                "Ошибка"
        )

        sys.exit(1)  # Завершаем программу с кодом ошибки


def check_task_exists(task_name):
    """
    Проверяет, существует ли задача в планировщике задач.

    :param task_name: Имя задачи для проверки.
    :return: True, если задача существует, иначе False.
    """

    try:
        # Выполняем команду для проверки существования задания
        command = ['schtasks', '/Query', '/TN', task_name]
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False


if __name__ == '__main__':
    run_as_admin()  # Проверяем и запускаем от имени администратора

    # Указываем имя задачи для проверки
    task_name = "Start CPG Monitor"
    # Проверяем, существует ли задача
    if check_task_exists(task_name):
        show_message_with_auto_close(
                f"Задача '{task_name}'\nуже существует в планировщике задач. Установка отменена.",
                "Предупреждение"
        )

        sys.exit()  # Завершаем выполнение, если задача уже существует
    else:
        run_powershell_commands()  # Выполняем команды PowerShell напрямую из Python

        sys.exit(1)  # Завершаем программу с кодом ошибки
