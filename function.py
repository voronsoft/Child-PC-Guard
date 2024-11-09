import ctypes
import hashlib
import hmac
import json
import os
import subprocess
import sys
import threading
import time
import winreg
import inspect

import psutil
import requests

from config_app import (
    DISK_LETTER,
    FOLDER_DATA,
    PATH_DATA_FILE,
    PATH_INSTALL_INFO_FILE,
    PATH_LOG_FILE,
    SECRET_KEY,
    path_bot_tg_exe,
)

FOLDER_DATA_PRGM_DATA = os.path.join(os.environ.get("PROGRAMDATA"), "Child PC Guard Data")
PATH_DATA_FILE_PRGM_DATA = os.path.join(FOLDER_DATA_PRGM_DATA, "data.json")
PATH_LOG_FILE_PRGM_DATA = os.path.join(FOLDER_DATA_PRGM_DATA, "log_chpcgu.txt")
PATH_INSTALL_INFO_FILE_PRGM_DATA = os.path.join(FOLDER_DATA_PRGM_DATA, "install_info.txt")


# ----------------------------------- Логирование ----------------------------
def log_error(message):
    """Метод для логирования ошибок в файл."""
    try:
        with open(PATH_LOG_FILE, "a", encoding="utf-8") as log_file:
            log_file.write(f"function.py({time.strftime('%Y-%m-%d %H:%M:%S')}) -" f" {message}\n==================\n")
    except Exception as e:
        print(f"Ошибка при записи лога в файл лога: {str(e)}")
        show_message_with_auto_close(
                f"function.py({time.strftime('%Y-%m-%d %H:%M:%S')}) - {message}\n==================\n", "Ошибка"
        )


# -------------------------------------- END ---------------------------------


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
                    0,  # 1-отобразить консоль \ 0-скрыть консоль
            )
            sys.exit()  # Завершаем текущий процесс, чтобы предотвратить двойной запуск
        except Exception as e:
            log_error(f"Не удалось запустить программу с правами администратора:\n{e}")
            show_message_with_auto_close(f"Не удалось запустить программу с правами администратора:\n{e}", "Ошибка")


def read_data_json(key, file_path=PATH_DATA_FILE):
    """
    Читает данные из JSON-файла и возвращает их в виде словаря.

    :param key: Ключ
    :param file_path: Путь к JSON-файлу.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            # Получаем данные из файла
            data = json.load(file)
        return data[key]
    except FileNotFoundError:
        log_error(f"Файл {file_path} не найден.")
        print(f"Файл {file_path} не найден.")
        return None
    except json.JSONDecodeError:
        log_error("Ошибка чтения JSON-файла.")
        print("Ошибка чтения JSON-файла.")
        return None
    except KeyError:
        log_error(f"Ключ '{key}' не найден в JSON-файле.")
        print(f"Ключ '{key}' не найден в JSON-файле.")
        return None


def update_data_json(key, value, file_path=PATH_DATA_FILE):
    """
    Изменяет данные в JSON-файле по указанному ключу и сохраняет их обратно в файл.

    :param key: Ключ, который нужно изменить или добавить.
    :param value: Новое значение для указанного ключа.
    :param file_path: Путь к JSON-файлу.
    """
    try:
        # Читаем текущие данные из файла
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)  # Читаем весь JSON-объект

        # Обновляем значение по указанному ключу
        if type(value) is int:
            data[key] = int(value)
        elif value.isdigit():
            data[key] = int(value)
        else:
            data[key] = str(value)

        # Сохраняем обновленные данные обратно в файл
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        return True
    except FileNotFoundError:
        log_error(f"Файл {file_path} не найден.")
        print(f"Файл {file_path} не найден.")
        return False
    except json.JSONDecodeError:
        log_error("Ошибка чтения JSON-файла.")
        print("Ошибка чтения JSON-файла.")
        return False
    except KeyError:
        log_error(f"Ключ '{key}' не найден в JSON-файле.")
        print(f"Ключ '{key}' не найден в JSON-файле.")
        return False
    except Exception as e:
        log_error(f"Ошибка при обновлении данных: {e}")
        print(f"Ошибка при обновлении данных: {e}")
        return False


def get_users():
    """Функция для получения списка пользователей из системы"""
    users = []
    netapi32 = ctypes.windll.netapi32
    bufptr = ctypes.c_void_p()
    entriesread = ctypes.c_ulong()
    totalentries = ctypes.c_ulong()

    # Получаем список пользователей
    res = netapi32.NetUserEnum(
            None,
            0,
            0,
            ctypes.byref(bufptr),
            ctypes.c_ulong(-1),
            ctypes.byref(entriesread),
            ctypes.byref(totalentries),
            None,
    )

    if res == 0:
        user_list = ctypes.cast(bufptr, ctypes.POINTER(ctypes.c_void_p * entriesread.value)).contents
        for i in range(entriesread.value):
            username = ctypes.cast(user_list[i], ctypes.c_wchar_p).value
            # Проверяем наличие домашнего каталога, чтобы исключить системные учетные записи
            if os.path.exists(os.path.join(DISK_LETTER, "Users", username)):
                users.append(username)

        netapi32.NetApiBufferFree(bufptr)
        if "администратор" in users:
            users.remove("администратор")
    return users


def get_block_user():
    """
    Получаем заблокированного пользователя

    :return str(username) or False if not user blocked
    """
    # Получение списка всех пользователей
    command = "net user"

    try:
        # Получаем список пользователей системы
        users = get_users()
        print("users:", users)
        # Получаем имя защищенного пользователя
        protect_usr = read_data_json("protected_user")
        print("protect_usr:", protect_usr)
        # Исключаем из списка пользователей системы защищенного пользователя
        if protect_usr in users:
            users.remove(protect_usr)

        print("2users:", users)

        disabled_users = []
        # Проверяем каждого пользователя, активна ли его учетная запись
        for user in users:
            user_info_command = f'net user "{user}"'
            user_info_result = subprocess.run(
                    user_info_command, capture_output=True, text=True, shell=True, encoding="cp866"
            )
            # print("user_info_result", user_info_result)
            user_info_output = user_info_result.stdout

            keyword_list = ["Account active", "Учетная запись активна", "Обліковий запис активний"]

            # Ищем строку активности учетной записи для разных языков
            if any(keyword in user_info_output for keyword in keyword_list):
                for line in user_info_output.splitlines():
                    # Проверяем для английской версии
                    if "Account active" in line and "No" in line:
                        disabled_users.append(user)
                        break
                    # Проверяем для русской версии
                    elif "Учетная запись активна" in line and "No" in line:
                        disabled_users.append(user)
                        break
                    # Проверяем для украинской версии
                    elif "Обліковий запис активний" in line and "No" in line:
                        disabled_users.append(user)
                        break
        # обновляем поле с именем
        log_error(f"(get_block_user()) переменная - disabled_users содержит:\n {disabled_users}")
        log_error(f"Возвращаемое значение: {disabled_users[0] if len(disabled_users[:]) != 0 else False}")

        return disabled_users[0] if len(disabled_users[:]) != 0 else False

    except Exception as e:
        log_error(f"(Function: get_block_user()) Произошла ошибка: {e}")
        return False


def get_session_id_by_username(username: str):
    """
    Получение данных сессии по имени пользователя

    :param username: Имя пользователя
    """
    try:
        # Выполняем команду `quser` и получаем её вывод
        command = "quser"  # Альтернатива команде `query user`
        result = subprocess.run(command, capture_output=True, shell=True, text=True, check=True, encoding="cp866")

        # Разбиваем вывод на строки и проходимся по каждой строке
        for line in result.stdout.splitlines():
            # Проверяем, содержится ли имя пользователя в строке
            if username.lower() in line.lower():  # Игнорируем регистр символов
                # Разбиваем строку по пробелам для получения элементов строки
                parts = line.split()
                if len(parts) >= 3 and parts[1].isdigit():  # если сессия не активна, но польз вошел в систему
                    return parts[:2]
                elif len(parts) >= 3 and parts[2].isdigit():  # если пользователь в сессии вошел в систему
                    return parts[:3]

        return None
    except subprocess.CalledProcessError as e:
        log_error(f"Ошибка получение данных сессии по имени пользователя\nОшибка:\n{e}")
        print(f"Ошибка получение данных сессии по имени пользователя\nОшибка:\n{e}")
    except Exception as e:
        log_error(f"Неизвестная ошибка: {e}")
        print(f"Неизвестная ошибка: {e}")
    return None


def is_session_active(usr_name):
    """
    Проверяет, активна ли сессия пользователя по имени.

    :param usr_name: Имя пользователя для проверки
    :return: True, если сессия активна; False, если неактивна
    """
    try:
        # Выполнение команды для получения информации о сессии пользователя
        command = f'query user {usr_name}'
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Обработка вывода команды
        for line in result.stdout.splitlines():
            # print(1)
            if usr_name in line:
                if "console" in line:
                    # print(2, "Сессия активна")
                    return True

            if usr_name not in line and usr_name in line:
                if "console" not in line:
                    # print(3, "Сессия НЕ активна")
                    return False

    except Exception as e:
        print(5, f"Произошла ошибка: {e}")

    # print(6, False)
    return False  # Если имя пользователя не найдено


def get_windows_edition_pro_or_home():
    """
    Получение названия редакции ОС

    - True: PRO версия
    - False: HOME версия
    - False: Если не то ни другое
    :return bool
    """
    try:
        # Открываем ключ реестра для получения информации о редакции Windows
        reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                 r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"
                                 )
        # Получаем значение редакции Windows
        edition, _ = winreg.QueryValueEx(reg_key, "ProductName")
        print("edition", edition, _)

        if "pro" in edition.lower():
            log_error(f"(get_windows_edition_pro_or_home()) Версия ос: {edition}")
            return True
        if "home" in edition.lower():
            log_error(f"(get_windows_edition_pro_or_home()) Версия ос: {edition}")
            return False
    except Exception as e:
        log_error(f"(get_windows_edition_pro_or_home()) Не удалось получить редакцию Windows:\n{e}")

    return False


# Windows PRO
def blocking(username, id_ses):
    """
    Функция блокировки пользователя. Для windows 10/11 PRO

    :param username: Имя блокируемого пользователя
    :param id_ses: ID сессии для блокировки экрана рабочего стола
    """
    # Статус запуска программы с привилегиями администратора или нет
    status_run = ctypes.windll.shell32.IsUserAnAdmin()
    log_error(f"0(blocking()) Статус запуска скрипта от имени Администратора: {status_run}")

    # Если запуск происходит от имени администратора
    if status_run:
        # Получаем имя пользователя активной сесии
        usr = os.getlogin()
        log_error(f"1(blocking()) Получаем имя пользователя текущей сессии: {usr}")

        # Получаем имя защищенного пользователя
        protect_usr = read_data_json("protected_user")
        log_error(f"2(blocking()) Получаем имя защищенного пользователя: {protect_usr}")

        # Получаем id активной сессии
        id_ses_active = ctypes.windll.kernel32.WTSGetActiveConsoleSessionId()
        log_error(f"3(blocking()) Получаем id текущей сессии: {id_ses_active}")

        # Если имя защищенного пользователя одинаково с именем блокируемого пользователя
        if protect_usr == usr:
            log_error("5(blocking()) Это сессия защищенного пользователя, команда блокировки ОТМЕНЕНА.")
            return
        # Если имя защищенного пользователя не совпадает с именем блокируемого пользователя
        elif protect_usr != usr:
            # Если сессия активна
            if is_session_active(usr):
                log_error("6(blocking()) Должна отработать блокировка")
                # --------------------------------------------------------------
                # Если id сессии не пустой
                if id_ses is not None:
                    # Команда выхода пользователя из сессии
                    command_logoff = f"logoff {id_ses}"
                    # Команда для блокировки учетной записи пользователя через PowerShell
                    command_disable_user = f'PowerShell -Command "Disable-LocalUser -Name \'{username}\'"'

                    # ------------------ Закрываем пользовательскую сессию -----------------------
                    try:
                        log_error(f"7(blocking()) Учетная запись {username} успешно заблокирована.")
                        # Выполнение команды через subprocess
                        result = subprocess.run(command_disable_user, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    except subprocess.CalledProcessError as e:
                        log_error(f"8(blocking()) Ошибка при выполнении команды блокировки учетки:\n{e.stderr}")
                    # ----------------------------------- END ------------------------------------
                    # ------------------------ Блокируем учетную запись --------------------------
                    try:
                        log_error("9(blocking()) Отработала команда блокировки экрана")
                        # Выполнение команды logoff для указанной сессии
                        subprocess.run(command_logoff, shell=True, check=True)
                    except Exception as e:
                        log_error(f"10(blocking()) Ошибка при выполнении команды выхода на экран блокировки:\n{e}")
                    # ----------------------------------- END ------------------------------------
                else:
                    log_error("11(blocking()) Не удалось получить ID сессии. Команды не будут выполнены.")
                # --------------------------------------------------------------
            # Сессия не активна
            else:
                log_error("12(blocking()) Пользователь не активировал сессию")
                return
    # Если нет прав Администратора на запуск, отмена операции
    else:
        log_error(f"13(blocking()) Отмена блокировки пользователя запущено НЕ от имени Администратора\n")


# Windows Home
def blocking_v2(username):
    """
    Функция блокировки пользователя. Для windows 10/11 HOME

    :param username: Имя блокируемого пользователя
    """
    # Статус запуска программы с привилегиями администратора или нет
    status_run = ctypes.windll.shell32.IsUserAnAdmin()
    log_error(f"0(blocking_v2()) Статус запуска скрипта от имени Администратора: {status_run}")

    # Если запуск происходит от имени администратора
    if status_run:
        # Получаем имя пользователя активной сесии
        usr_ses = os.getlogin()
        log_error(f"1(blocking_v2()) Получаем имя пользователя текущей сессии: {usr_ses}")

        # Получаем имя защищенного пользователя
        protect_usr = read_data_json("protected_user")
        log_error(f"2(blocking_v2()) Получаем имя защищенного пользователя: {protect_usr}")

        # Если имя защищенного пользователя одинаково с именем пользователя активной сессии
        if protect_usr == usr_ses:
            log_error("5(blocking_v2()) Это сессия защищенного пользователя, команда блокировки ОТМЕНЕНА.")
            # Открытие окна с сообщением
            ctypes.windll.user32.MessageBoxW(0, "Это сессия защищенного пользователя, команда блокировки ОТМЕНЕНА.",
                                             "Отмена операции", 0
                                             )
            return
        # Если имя защищенного пользователя не совпадает с именем блокируемого пользователя
        elif protect_usr != usr_ses:
            log_error("6(blocking_v2()) Должна отработать блокировка")
            # ------------------ Блокируем учетную запись -----------------------
            try:
                # Команда блокировки учетной записи пользователя (Windows HOME)
                command_disable_user = f"net user {username} /active:no"
                # Выполнение команды блокировки учётки от имени администратора
                # subprocess.run(['runas', '/user:Administrator', f'cmd /c {command_disable_user}'], shell=True, check=True)
                subprocess.run(command_disable_user, shell=True, check=True)

                log_error(f"7(blocking_v2()) Учетная запись {username} успешно заблокирована.")
            except subprocess.CalledProcessError as e:
                log_error(f"8(blocking_v2()) Ошибка при выполнении команды блокировки учётки:\n{str(e)}")
            except Exception as e:
                log_error(f"8(blocking_v2()) Ошибка при выполнении команды блокировки учётки:\n{str(e)}")
            # ----------------------------------- END ------------------------------------
            # ------------------------ Закрываем пользовательскую сессию --------------------------
            try:
                # Команда выхода из сессии пользователя (Windows HOME)
                command_logoff = f"shutdown /l"
                # Выполнение команды выхода из сессии
                # subprocess.run(['runas', '/user:Administrator', f'cmd /c {command_logoff}'], shell=True, check=True)
                subprocess.run(command_logoff, shell=True, check=True)
                log_error("9(blocking_v2()) Отработала команда блокировки экрана")
            except subprocess.CalledProcessError as e:
                log_error(f"10(blocking_v2()) Ошибка при выполнении команды выхода на экран блокировки:\n{str(e)}")
            except Exception as e:
                log_error(f"10(blocking_v2()) Ошибка при выполнении команды выхода на экран блокировки:\n{str(e)}")
            # ----------------------------------- END ------------------------------------
    # Если нет прав Администратора на запуск, отмена операции
    else:
        log_error(f"13(blocking_v2()) Отмена блокировки пользователя запущено НЕ от имени Администратора\n")


def username_session():
    """Получение имени пользователя в активной сессии"""
    username_session = os.getlogin()  # Получение имени текущего пользователя
    return username_session


def show_message_with_auto_close(message="Тестовое сообщение", title="Сообщение", delay=3):
    """
    Показывает сообщение в окне и закрывает его через заданное количество секунд.

    :param message: Сообщение для отображения
    :param title: Заголовок окна (по умолчанию "Сообщение")
    :param delay: Время задержки перед закрытием (в секундах), по умолчанию 5 секунд
    """

    # Функция для отображения сообщения
    def display_message():
        ctypes.windll.user32.MessageBoxW(None, message, title, 0)

    # Функция для автоматического закрытия окна
    def auto_close():
        # Ждем указанное количество секунд
        time.sleep(delay)
        # Ищем окно по заголовку
        hwnd = ctypes.windll.user32.FindWindowW(None, title)
        if hwnd:
            # Отправляем команду на закрытие окна (WM_CLOSE)
            ctypes.windll.user32.PostMessageW(hwnd, 0x0010, 0, 0)  # 0x0010 — это WM_CLOSE
        else:
            print(f"Окно с заголовком '{title}' не найдено.")

    # Запускаем отображение сообщения и авто-закрытие в отдельных потоках
    threading.Thread(target=display_message).start()
    threading.Thread(target=auto_close).start()


def function_to_create_path_data_files():
    """Функция проверки и создания файлов данных для приложения"""
    # Проверяем, существует ли папка. Если нет, то создаем её.
    if not os.path.exists(FOLDER_DATA):
        os.makedirs(FOLDER_DATA)
        print(f"Создана папка: {FOLDER_DATA}")
        log_error(f"Создана папка: {FOLDER_DATA}")

        # Применяем полные права ко всем пользователям на созданную папку
        subprocess.run(
                ["icacls", FOLDER_DATA, "/grant", "Everyone:F", "/T", "/C"],
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
        )
        # /grant - предоставить права
        # Everyone:F - разрешить полные права для всех пользователей
        # /T - рекурсивно для всех вложенных файлов и папок
        # /C - продолжить выполнение даже при ошибках
        print(f"Права доступа установлены для папки: {FOLDER_DATA}")
        log_error(f"Права доступа установлены для папки: {FOLDER_DATA}")

    # Проверяем, существует ли файл data.json. Если нет, то создаем его и записываем начальные данные.
    if not os.path.exists(PATH_DATA_FILE):
        initial_data = {
                "username_blocking": "",
                "remaining_time": 0,
                "date": "0001-02-03",
                "protected_user": "",
                "bot_token_telegram": "7456533985:AAEGOk3VUU04Z4bk9B83kzy4MW5zem3hbYw",
                "chat_id": 631191214,
                "language": "uk",
        }
        with open(PATH_DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(initial_data, file, indent=4)  # Записываем данные в формате JSON с отступами
        print(f"Создан файл: {PATH_DATA_FILE} с начальными данными")
        log_error(f"Создан файл: {PATH_DATA_FILE} с начальными данными")

    # Проверяем, существует ли файл log_chpcgu.txt. Если нет, то создаем его.
    if not os.path.exists(PATH_LOG_FILE):
        with open(PATH_LOG_FILE, "w", encoding="utf-8") as file:
            file.write("")  # Создаем пустой лог-файл
        print(f"Создан файл: {PATH_LOG_FILE}")
        log_error(f"Создан файл: {PATH_LOG_FILE}")

    # Проверяем, существует ли файл install_info.txt. Если нет, то создаем его.
    if not os.path.exists(PATH_INSTALL_INFO_FILE):
        with open(PATH_INSTALL_INFO_FILE, "w", encoding="utf-8") as file:
            file.write("")  # Создаем пустой лог-файл
        print(f"Создан файл: {PATH_INSTALL_INFO_FILE}")
        log_error(f"Создан файл: {PATH_INSTALL_INFO_FILE}")

    # Применяем полные права ко всем пользователям на файлы, если они уже существуют или только что были созданы.
    # Задаем доступ для всех на запись чтение изменение.
    subprocess.run(
            ["icacls", FOLDER_DATA, "/grant", "Everyone:F", "/T", "/C"],
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
    )
    # print(f"Права доступа обновлены для папки и вложенных файлов: {FOLDER_DATA}")
    log_error(f"Права доступа обновлены для папки и вложенных файлов: {FOLDER_DATA}")
    #
    # -------------------------------------------------------------------------------------
    # TODO В момент релиза можно удалить эту часть кода, необходим в момент разработки при запуске exe файлов
    # -------------------------------------------------------------------------------------
    #
    if not os.path.exists(FOLDER_DATA_PRGM_DATA):
        os.makedirs(FOLDER_DATA_PRGM_DATA)
        print(f"2Создана папка: {FOLDER_DATA_PRGM_DATA}")
        log_error(f"2Создана папка: {FOLDER_DATA_PRGM_DATA}")

        # Применяем полные права ко всем пользователям на созданную папку
        subprocess.run(
                ["icacls", FOLDER_DATA_PRGM_DATA, "/grant", "Everyone:F", "/T", "/C"],
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
        )
        # /grant - предоставить права
        # Everyone:F - разрешить полные права для всех пользователей
        # /T - рекурсивно для всех вложенных файлов и папок
        # /C - продолжить выполнение даже при ошибках
        # print(f"2Права доступа установлены для папки: {FOLDER_DATA_PRGM_DATA}")
        log_error(f"2Права доступа установлены для папки: {FOLDER_DATA_PRGM_DATA}")

    # Проверяем, существует ли файл data.json. Если нет, то создаем его и записываем начальные данные.
    if not os.path.exists(PATH_DATA_FILE_PRGM_DATA):
        initial_data = {
                "username_blocking": "",
                "remaining_time": 0,
                "date": "0001-02-03",
                "protected_user": "",
                "bot_token_telegram": "7456533985:AAEGOk3VUU04Z4bk9B83kzy4MW5zem3hbYw",
                "chat_id": 631191214,
                "language": "uk",
        }
        with open(PATH_DATA_FILE_PRGM_DATA, "w", encoding="utf-8") as file:
            json.dump(initial_data, file, indent=4)  # Записываем данные в формате JSON с отступами
        print(f"2Создан файл: {PATH_DATA_FILE_PRGM_DATA} с начальными данными")
        log_error(f"2Создан файл: {PATH_DATA_FILE_PRGM_DATA} с начальными данными")

    # Проверяем, существует ли файл log_chpcgu.txt. Если нет, то создаем его.
    if not os.path.exists(PATH_LOG_FILE_PRGM_DATA):
        with open(PATH_LOG_FILE_PRGM_DATA, "w", encoding="utf-8") as file:
            file.write("")  # Создаем пустой лог-файл
        print(f"2Создан файл: {PATH_LOG_FILE_PRGM_DATA}")
        log_error(f"2Создан файл: {PATH_LOG_FILE_PRGM_DATA}")

    # Проверяем, существует ли файл install_info.txt. Если нет, то создаем его.
    if not os.path.exists(PATH_INSTALL_INFO_FILE_PRGM_DATA):
        with open(PATH_INSTALL_INFO_FILE_PRGM_DATA, "w", encoding="utf-8") as file:
            file.write("")  # Создаем пустой лог-файл
        print(f"2Создан файл: {PATH_INSTALL_INFO_FILE_PRGM_DATA}")
        log_error(f"2Создан файл: {PATH_INSTALL_INFO_FILE_PRGM_DATA}")

    # Применяем полные права ко всем пользователям на файлы, если они уже существуют или только что были созданы.
    # Задаем доступ для всех на запись чтение изменение.
    subprocess.run(
            ["icacls", FOLDER_DATA_PRGM_DATA, "/grant", "Everyone:F", "/T", "/C"],
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
    )
    # print(f"2 Права доступа обновлены для папки и файлов: {FOLDER_DATA_PRGM_DATA}")
    log_error(f"2Права доступа обновлены для папки и вложенных файлов: {FOLDER_DATA_PRGM_DATA}")


def check_mode_run_app():
    """Проверяет, запущено ли приложение от имени администратора."""
    try:
        if os.name == "nt":
            app_is_admin = bool(ctypes.windll.shell32.IsUserAnAdmin())
            return "admin" if app_is_admin else "user"
    except:
        log_error(f"Запуск приложения в режиме ПОЛЬЗОВАТЕДЬ")
    return "user"


def check_if_program_running(program_name):
    """Проверка сатуса работы программы в Windows"""
    # Получаем список всех запущенных процессов
    for process in psutil.process_iter(["pid", "name"]):
        try:
            # Сравниваем имя процесса с искомым
            if process.info["name"].lower() == program_name.lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


def seconds_to_hms(seconds):
    """
    Преобразует количество секунд в строку формата часы:минуты:секунды.

    :param seconds: Количество секунд (целое число).
    :return: Строка формата "часы:минуты:секунды".
    """
    # Вычисляем количество часов, минут и секунд
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    # Форматируем результат с ведущими нулями
    return f"{hours:02}:{minutes:02}:{secs:02}"


def show_warning_message(msg_txt: str):
    """
    Вывод окна с предупреждением на рабочий стол

    :param msg_txt:
    :return: True/False
    """
    show_message_with_auto_close()


def kill_program_by_name(program_name="run_bot_telegram.exe"):
    """
    Закрывает все процессы с указанным именем программы.
    По умолчанию ищет программу бота телеграм. (run_bot_telegram.exe)

    :param program_name: Имя исполняемого файла программы (например, "example.exe").
    """
    # Проходим по всем процессам в системе
    for proc in psutil.process_iter(["pid", "name"]):
        try:
            # Проверяем, совпадает ли имя процесса с указанным
            if proc.info["name"].lower() == program_name.lower():
                print(f"Закрываю процесс: {proc.info['name']} (PID: {proc.info['pid']})")
                proc.terminate()  # Завершаем процесс
                proc.wait()  # Ожидаем завершения процесса
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Игнорируем ошибки, если процесс уже завершен или недоступен
            pass


# --------------------------Работа с паролем для приложения-------------------
def hash_password(password: str) -> str:
    """Хеширует пароль с использованием HMAC и секретного ключа."""
    hash_psw = hmac.new(SECRET_KEY.encode("utf-8"), password.encode("utf-8"), hashlib.sha256).hexdigest()
    return hash_psw


def check_password(input_password: str, stored_hashed_password: str) -> bool:
    """
    Сравнивает хеш введённого пароля с хранимым хешем.

    :param input_password: Пароль из поля
    :param stored_hashed_password: Пароль из БД
    :return:
    """
    hashed_input = hash_password(input_password)
    return hashed_input == stored_hashed_password


# -------------------------------- Работа с реестром -------------------------
# Путь в реестре - Компьютер\HKEY_LOCAL_MACHINE\SOFTWARE\CPG_Password
def set_password_in_registry(password: str):
    """Записывает пароль в реестр."""
    # Путь в реестре - Компьютер-HKEY_LOCAL_MACHINE-SOFTWARE-CPG_Password
    key_path = r"Software\CPG_Password"

    # Открываем или создаем ключ реестра
    try:
        key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key_path)
        winreg.SetValueEx(key, "Password", 0, winreg.REG_SZ, password)
        winreg.CloseKey(key)
        print("Пароль успешно сохранен в реестр.")
        log_error("Пароль успешно сохранен в реестр.")
    except Exception as e:
        print(f"Ошибка при записи пароля в реестр: {e}")
        log_error(f"(set_password_in_registry) Ошибка при записи пароля в реестр:\n{e}")


def get_password_from_registry():
    """Читает пароль из реестра."""
    key_path = r"Software\CPG_Password"

    try:
        # Открываем ключ реестра
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path)
        password, _ = winreg.QueryValueEx(key, "Password")
        winreg.CloseKey(key)
        return password
    except FileNotFoundError:
        print("Пароль не найден в реестре.")
        log_error("Пароль не найден в реестре.")
        return False
    except Exception as e:
        print(f"Ошибка при чтении пароля из реестра: {e}")
        log_error(f"(get_password_from_registry) Ошибка при чтении пароля из реестра:\n{e}")
        return False


def delete_password_from_registry():
    """Удаляет запись пароля из реестра."""
    key_path = r"Software\CPG_Password"

    try:
        # Открываем ключ реестра с правами на запись
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, "Password")
        winreg.CloseKey(key)
        print("Пароль удален из реестра.")
        log_error("Пароль удален из реестра.")
    except FileNotFoundError:
        print("Запись не найдена в реестре.")
        log_error("(get_password_from_registry) Запись не найдена в реестре.")
    except Exception as e:
        print(f"Ошибка при удалении записи пароля: {e}")
        log_error(f"Ошибка при удалении записи пароля: {e}")


# ----------------------------------- Работа с BOT telegram---------------------------
def send_bot_telegram_message(
        message="Default message.", bot_token=read_data_json("bot_token_telegram"), chat_id=read_data_json("chat_id")
):
    """
    Отправляет сообщение в Telegram через указанный бот.
    :param message: Сообщение, которое нужно отправить.
    :param bot_token: Токен Telegram-бота.
    :param chat_id: ID чата, куда будет отправлено сообщение.
    :return: None
    """
    # URL для отправки сообщения
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    # Данные, которые будут отправлены
    data = {
            "chat_id": chat_id,
            "text": message,
    }

    # Отправка POST-запроса к API Telegram
    response = requests.post(url, data=data)

    # Проверка ответа от Telegram
    if response.status_code == 200:
        log_error(f"MSG -> BOT:\n{message}")
    else:
        log_error(f"Ошибка при отправке сообщения: {response.status_code} - {response.text}")


def run_program_bot():
    """Запускает программу бота телеграм"""
    try:
        subprocess.Popen(path_bot_tg_exe)  # Запускаем программу
        log_error("Бот запущен при старте основного приложения")
    except Exception as e:
        log_error(f"Ошибка при запуске программы Бота:\n{e}")


# -------------------------------------- END ---------------------------------


# ------------------------- Работа с Дескриптором мьютекса --------------------
def process_mutex_error(error_code, mutex):
    """Функция для обработки ошибок, связанных с мьютексом и кодом ошибки."""
    # Получение файла, в котором функция была вызвана
    caller_frame = inspect.stack()[1]
    caller_file = os.path.basename(caller_frame.filename)

    if error_code == 183:  # Объект с таким именем уже существует.
        log_error(f"({caller_file}) Error mutex: {error_code}\n"
                  f"The application is already running. A second instance of the application cannot be launched."
                  )
        sys.exit()

    elif error_code == 5:  # ERROR_ACCESS_DENIED
        print(2)
        if mutex != 0:
            log_error(f"({caller_file}) ERROR: Access to mutex is denied.")
        return

    elif error_code != 0:  # Обработка других ошибок
        print(4)
        if mutex != 0:
            log_error(f"({caller_file}) ERROR: Unknown error {error_code}")
            sys.exit()
        return


# --------------------------------------- END ---------------------------------

if __name__ == "__main__":
    username = "test"  # Получаем имя пользователя для блокировки
    session_data = get_session_id_by_username(username)  # Данные о сессии
    id_session_username = int(*(id for id in session_data if id.isdigit()))  # ID сессии

    print("username- ", username)
    print("session_data- ", session_data)
    print("id_session_username- ", id_session_username)
