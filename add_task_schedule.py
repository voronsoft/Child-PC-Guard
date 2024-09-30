# Файл отвечает за автоматизацию процесса добавления задания (для запуска мониторинга за программой Child PC Guard),
# в планировщик заданий.
#
import os
import sys
import time
import ctypes
import subprocess

# Определяем корневую папку проекта
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
# Получаем имя диска (вид С:\)
DISK_LETTER = os.path.splitdrive(PROJECT_ROOT)[0] + "\\"
# Путь к папке с данными
FOLDER_DATA = os.path.join(DISK_LETTER, "ProgramData", "Child PC Guard Data")
# Путь к файлу логов - log_chpcgu.txt
path_log_file = os.path.join(FOLDER_DATA, "log_chpcgu.txt")


# ---------------------
def log_error(message):
    """Метод для логирования ошибок в файл."""
    try:
        with open(path_log_file, 'a', encoding='utf-8') as log_file:
            log_file.write(f"ADD_TASK_SCHEDULE({time.strftime('%Y-%m-%d %H:%M:%S')}) -"
                           f" {message}\n==================\n"
                           )
    except Exception as e:
        print(f"Ошибка при записи лога в файл лога: {str(e)}")
        ctypes.windll.user32.MessageBoxW(
                None,
                f"function.py({time.strftime('%Y-%m-%d %H:%M:%S')}) - {message}\n==================\n",
                "Ошибка",
                0
        )


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
            ctypes.windll.user32.MessageBoxW(
                    None,
                    f"Не удалось запустить программу с правами администратора:\n\n{e}",
                    "Ошибка",
                    0
            )


def run_powershell_script(script_path):
    """
    Запускает PowerShell для изменения политики выполнения и запуска указанного скрипта.

    :param script_path: Путь к скрипту PowerShell для выполнения.
    """
    # Формируем команду PowerShell для изменения политики и запуска скрипта
    command = (
            f"Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process; "
            f"& '{script_path}'"
    )

    try:
        # Запускаем PowerShell с указанной командой
        subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", command], check=True)
        print("Скрипт успешно выполнен с правами администратора.")
    except subprocess.CalledProcessError as e:
        print(f"Произошла ошибка при выполнении скрипта: {e}")


if __name__ == '__main__':
    run_as_admin()  # Проверяем и запускаем от имени администратора

    # Указываем путь к скрипту task_schedule_import_powershell.ps1
    script_path = os.path.join(PROJECT_ROOT, "task_schedule_import_powershell.ps1")

    # Проверяем, существует ли файл
    if os.path.isfile(script_path):
        run_powershell_script(script_path)  # Запускаем скрипт PowerShell
    else:
        print(f"Скрипт не найден по пути: {script_path}")
