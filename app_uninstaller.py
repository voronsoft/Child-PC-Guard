import ctypes
import os
import shutil
import subprocess
import sys
import time
import winreg

import psutil


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
                # TODO отобразить окно консоли или скрыть
                1,  # 1-отобразить консоль \ 0-скрыть консоль
            )
            sys.exit()  # Завершаем текущий процесс, чтобы предотвратить двойной запуск
        except Exception as e:
            pass


# Функция для завершения процесса
def kill_process(process_name):
    try:
        # Проверяем, активен ли процесс
        for proc in psutil.process_iter(["name"]):
            if proc.info["name"] == process_name:
                # Завершаем процесс принудительно
                subprocess.run(["taskkill", "/F", "/IM", process_name], check=True, shell=True)
                print(f"Процесс {process_name} завершён.\n")
                return True
        print(f"Процесс {process_name} не найден.")
    except Exception as e:
        print(f"Ошибка при завершении процесса {process_name}: {e}")
    return False


# Функция для удаления файла, если он существует
def delete_file(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Файл {file_path} удалён.")
        else:
            print(f"Файл {file_path} не найден.")
    except Exception as e:
        print(f"Ошибка при удалении файла {file_path}: {e}")


# Функция удаления записи с реестра
def delete_registry_key(key_path=r"SOFTWARE\CPG_Password"):
    try:
        # Открываем корневой раздел реестра для работы с 64-битным разделом
        reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_WOW64_64KEY | winreg.KEY_ALL_ACCESS)

        # Удаляем ключ
        winreg.DeleteKey(reg_key, "")

        # Закрываем раздел реестра
        winreg.CloseKey(reg_key)

        print(f"Ключ реестра '{key_path}' успешно удалён.\n")

    except FileNotFoundError:
        print(f"Ключ реестра '{key_path}' не найден.\n")
    except PermissionError:
        print(
            f"Недостаточно прав для удаления ключа '{key_path}'. Попробуйте запустить скрипт с правами администратора."
        )
    except Exception as e:
        print(f"Ошибка при удалении ключа реестра '{key_path}': {e}")


# Функция удаления записи с реестра Об инсталляторе
def remove_specific_registry_key():
    # Путь к ключу реестра и имя удаляемого ключа
    key_path = r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    subkey_name = "Child PC Guard Suite_is1"

    try:
        # Открываем ключ реестра по указанному пути
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_ALL_ACCESS) as key:
            # Удаляем подключ по его имени
            winreg.DeleteKey(key, subkey_name)
            print(f'Запись "{subkey_name}" успешно удалена из реестра.')
    except FileNotFoundError:
        print(f'Запись "{subkey_name}" не найдена.')
    except PermissionError:
        print(f"Недостаточно прав для удаления записи. Запустите скрипт от имени администратора.")
    except Exception as e:
        print(f"Произошла ошибка при удалении записи: {e}")


# Функция удаления задания из планировщика задач
def delete_task(task_name=r"Start CPG Monitor"):
    try:
        # Выполнение команды для удаления задания из планировщика задач
        subprocess.run(f'schtasks /Delete /TN "{task_name}" /F', check=True, shell=True)
        print(f"Задание '{task_name}' успешно удалено из планировщика задач.\n")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при удалении задания '{task_name}': {e}\n")


# Функция удаления ярлыков приложения
def delete_all_shortcuts():
    try:
        # Список ярлыков из меню "Пуск"
        start_menu_shortcuts = [
            r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Child PC Guard\Child PC Guard.lnk",
            r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Child PC Guard\Child PC Timer.lnk",
            r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Child PC Guard\Child PC Unlock User.lnk",
            r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Child PC Guard\Child PC Monitor.lnk",
            r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Child PC Guard\Logs Child PC Guard.lnk",
        ]

        # Список ярлыков с рабочего стола
        desktop_shortcuts = [
            r"C:\Users\Public\Desktop\Child PC Timer.lnk",
            r"C:\Users\Public\Desktop\Child PC Guard.lnk",
        ]

        # Объединяем все ярлыки в один список
        all_shortcuts = start_menu_shortcuts + desktop_shortcuts

        # Проходим по каждому ярлыку и пытаемся удалить
        for shortcut in all_shortcuts:
            if os.path.exists(shortcut):
                os.remove(shortcut)
                print(f"Ярлык '{shortcut}' успешно удалён.")
            else:
                print(f"Ярлык '{shortcut}' не найден.")

        print("\n")

    except Exception as e:
        print(f"Ошибка при удалении ярлыков: {e}\n")


# Функция удаления папки данных приложения
def delete_folder_and_files(folder_path=r"C:\ProgramData\Child PC Guard Data"):
    try:
        # Проверяем, существует ли папка
        if os.path.exists(folder_path):
            # Удаляем все файлы внутри папки
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)  # Удалить файл или ссылку
                        print(f"Файл '{file_path}' успешно удалён.")
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)  # Удалить вложенную папку и её содержимое
                        print(f"Папка '{file_path}' и её содержимое успешно удалены.")
                except Exception as e:
                    print(f"Ошибка при удалении '{file_path}': {e}")
            print("\n")

            # Удаляем саму папку после того, как все файлы были удалены
            os.rmdir(folder_path)
            print(f"Папка '{folder_path}' успешно удалена.")
        else:
            print(f"Папка '{folder_path}' не найдена.")
    except Exception as e:
        print(f"Ошибка при удалении папки '{folder_path}': {e}")


# Функция удаления папки приложения
def delete_folder_and_contents(folder_path=r"C:\Program Files (x86)\Child PC Guard"):
    try:
        # Проверяем, существует ли папка
        if os.path.exists(folder_path):
            # Удаляем папку и всё её содержимое
            shutil.rmtree(folder_path)
            print(f"Папка '{folder_path}' и всё её содержимое успешно удалены.")
        else:
            print(f"Папка '{folder_path}' не найдена.")
    except Exception as e:
        print(f"Ошибка при удалении папки '{folder_path}': {e}\n")


def uninstaller():
    # Перезапуск деинсталлятора с правами администратора
    run_as_admin()

    # Удаления задания из планировщика задач
    delete_task()

    # Удаление записи с реестра
    delete_registry_key("SOFTWARE\\CPG_Password")

    # Удаление записи с реестра Об инсталляторе
    remove_specific_registry_key()

    # Вызов функции для удаления всех ярлыков
    delete_all_shortcuts()

    # ----------------------------------------------------
    # Список процессов и путей к исполняемым файлам
    processes = {
        "Windows CPG Monitor.exe": r"C:\Program Files (x86)\Child PC Guard\Windows CPG Monitor.exe",
        "Child PC Guard.exe": r"C:\Program Files (x86)\Child PC Guard\Child PC Guard.exe",
        "run_bot_telegram.exe": r"C:\Program Files (x86)\Child PC Guard\run_bot_telegram.exe",
        "Child PC Timer.exe": r"C:\Program Files (x86)\Child PC Guard\Child PC Timer.exe",
        "Child PC Unlock User.exe": r"C:\Program Files (x86)\Child PC Guard\Child PC Unlock User.exe",
    }

    # Завершаем процессы и удаляем приложения (исполняемые файлы)
    for process, file_path in processes.items():
        print(f"Попытка завершить процесс {process}...")
        process_killed = kill_process(process)

        # Подождём немного перед удалением файла
        time.sleep(1)

        if process_killed:
            print(f"Попытка удалить файл {file_path}...")
            delete_file(file_path)
        else:
            print(f"Пропуск удаления файла {file_path}, так как процесс не был найден.")

        print("\n")

    # ----------------------------------------------------

    # Удаляем папку с данными и всем ее содержимым
    delete_folder_and_files()

    # Удаляем папку приложения
    delete_folder_and_contents()


if __name__ == "__main__":
    uninstaller()
