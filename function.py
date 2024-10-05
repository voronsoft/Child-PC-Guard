import hashlib
import hmac
import os
import sys
import time
import json
import winreg
import ctypes
import threading
import subprocess

from config_app import FOLDER_DATA, PATH_DATA_FILE, PATH_LOG_FILE, PATH_INSTALL_INFO_FILE, SECRET_KEY


# ----------------------------------- Логирование ----------------------------
def log_error(message):
    """Метод для логирования ошибок в файл."""
    try:
        with open(PATH_LOG_FILE, 'a', encoding='utf-8') as log_file:
            log_file.write(f"function.py({time.strftime('%Y-%m-%d %H:%M:%S')}) -"
                           f" {message}\n==================\n"
                           )
    except Exception as e:
        print(f"Ошибка при записи лога в файл лога: {str(e)}")
        show_message_with_auto_close(f"function.py({time.strftime('%Y-%m-%d %H:%M:%S')}) - {message}\n==================\n",
                                     "Ошибка"
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
                    ' '.join([f'"{arg}"' for arg in sys.argv]),
                    None,
                    # TODO отобразить окно консоли или скрыть
                    1  # 1-отобразить консоль \ 0-скрыть консоль
            )
            sys.exit()  # Завершаем текущий процесс, чтобы предотвратить двойной запуск
        except Exception as e:
            log_error(f"Не удалось запустить программу с правами администратора:\n{e}")
            show_message_with_auto_close(
                    f"Не удалось запустить программу с правами администратора:\n\n{e}",
                    "Ошибка"
            )


def read_json(key, file_path=PATH_DATA_FILE):
    """
    Читает данные из JSON-файла и возвращает их в виде словаря.

    :param key: Ключ
    :param file_path: Путь к JSON-файлу.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
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


def update_json(key, value, file_path=PATH_DATA_FILE):
    """
    Изменяет данные в JSON-файле по указанному ключу и сохраняет их обратно в файл.

    :param key: Ключ, который нужно изменить или добавить.
    :param value: Новое значение для указанного ключа.
    :param file_path: Путь к JSON-файлу.
    """
    try:
        # Читаем текущие данные из файла
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)  # Читаем весь JSON-объект

        # Обновляем значение по указанному ключу
        if type(value) is int:
            data[key] = int(value)
        elif value.isdigit():
            data[key] = int(value)
        else:
            data[key] = str(value)

        # Сохраняем обновленные данные обратно в файл
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        print(f"Данные успешно обновлены: {key} = {value}")

    except FileNotFoundError:
        log_error(f"Файл {file_path} не найден.")
        print(f"Файл {file_path} не найден.")
    except json.JSONDecodeError:
        log_error("Ошибка чтения JSON-файла.")
        print("Ошибка чтения JSON-файла.")
    except KeyError:
        log_error(f"Ключ '{key}' не найден в JSON-файле.")
        print(f"Ключ '{key}' не найден в JSON-файле.")
    except Exception as e:
        log_error(f"Ошибка при обновлении данных: {e}")
        print(f"Ошибка при обновлении данных: {e}")


def get_users():
    """Функция для получения списка пользователей из системы"""
    users = []
    netapi32 = ctypes.windll.netapi32
    bufptr = ctypes.c_void_p()
    entriesread = ctypes.c_ulong()
    totalentries = ctypes.c_ulong()

    # Получаем список пользователей
    res = netapi32.NetUserEnum(
            None, 0, 0, ctypes.byref(bufptr),
            ctypes.c_ulong(-1), ctypes.byref(entriesread), ctypes.byref(totalentries), None
    )

    if res == 0:
        user_list = ctypes.cast(bufptr, ctypes.POINTER(ctypes.c_void_p * entriesread.value)).contents
        for i in range(entriesread.value):
            username = ctypes.cast(user_list[i], ctypes.c_wchar_p).value
            # Проверяем наличие домашнего каталога, чтобы исключить системные учетные записи
            if os.path.exists(f"C:\\Users\\{username}"):
                users.append(username)
        netapi32.NetApiBufferFree(bufptr)
    return users


def get_block_user():
    """Получаем заблокированного пользователя"""
    # Выполняем команду для получения списка всех пользователей
    command = 'net user'

    try:
        # Выполняем команду и получаем список всех пользователей
        result = subprocess.run(command, capture_output=True, text=True, shell=True, encoding='cp866')

        # Ищем пользователей в выводе команды
        users = get_users()
        disabled_users = []

        # Проверяем каждого пользователя, активна ли его учетная запись
        for user in users:
            user_info_command = f'net user "{user}"'
            user_info_result = subprocess.run(user_info_command,
                                              capture_output=True,
                                              text=True,
                                              shell=True,
                                              encoding='cp866'
                                              )
            user_info_output = user_info_result.stdout

            keyword_list = ['Account active', 'Учетная запись активна', 'Обліковий запис активний']

            # Ищем строку активности учетной записи для разных языков
            if any(keyword in user_info_output for keyword in keyword_list):
                for line in user_info_output.splitlines():
                    # Проверяем для английской версии
                    if 'Account active' in line and 'No' in line:
                        disabled_users.append(user)
                        break
                    # Проверяем для русской версии
                    elif 'Учетная запись активна' in line and 'No' in line:
                        disabled_users.append(user)
                        break
                    # Проверяем для украинской версии
                    elif 'Обліковий запис активний' in line and 'No' in line:
                        disabled_users.append(user)
                        break
        # обновляем поле с именем
        return disabled_users[0]

    except Exception as e:
        log_error(f"Произошла ошибка: {e}")
        return ""


def get_session_id_by_username(username: str):
    """
    Получение данных сессии по имени пользователя

    :param username: Имя пользователя
    """
    try:
        # Выполняем команду `quser` и получаем её вывод
        command = 'quser'  # Альтернатива команде `query user`
        result = subprocess.run(command, capture_output=True, shell=True, text=True, check=True, encoding='cp866')

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


def blocking(username, id_ses_user):
    """
    Функция блокировки пользователя.

    :param username: Имя блокируемого пользователя
    :param id_sess_user: ID сессии для блокировки экрана рабочего стола
    """
    if id_ses_user is not None:
        command_logoff = f"logoff {id_ses_user}"
        command_disable_user = f'net user "{username}" /active:no'
        try:
            # Выполнение команды logoff для указанной сессии
            subprocess.run(command_logoff, shell=True, check=True)
            print("1 Отработала команда блокировки экрана")
            time.sleep(1)
            # TODO закомментированная команда для теста
            # Выполняем команду для блокировки учетной записи
            subprocess.run(command_disable_user, shell=True, check=True)
            print("2 Отработала команда блокировки учетной записи")
            print(f"Учетка заблокирована {username} (ID: {id_ses_user}).")
        except subprocess.CalledProcessError as e:
            log_error(f"Ошибка при выполнении команд: {e}")
            print(f"Ошибка при выполнении команд: {e}")
    else:
        print("Не удалось получить ID сессии. Команды не будут выполнены.")


def unblock_user(username):
    """
    Разблокирует учетную запись пользователя Windows.

    :param username: Имя учетной записи пользователя для разблокировки.
    """
    try:
        # Формируем команду для разблокировки пользователя
        command = f'net user "{username}" /active:yes'
        # Выполняем команду в командной строке
        subprocess.run(command, shell=True, check=True)
        return True
    except Exception as e:
        log_error(f"Ошибка при разблокировке пользователя - {username}:\n\n{e}")
        show_message_with_auto_close(f"Ошибка при разблокировке пользователя - {username}:\n\n{e}",
                                     "Ошибка"
                                     )
        return False


def username_session():
    """Получение имени пользователя в сессии"""
    username_session = os.getlogin()  # Получение имени текущего пользователя
    return username_session


def show_message_with_auto_close(message, title="Сообщение", delay=3):
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


# TODO Поправить пути исходя из данных куда было установленно приложение пользователем (динамические ссылки на
#  приложения)
def function_to_create_path_data_files():
    """Функция проверки и создания файлов данных для приложения"""

    # Проверяем, существует ли папка. Если нет, то создаем её.
    if not os.path.exists(FOLDER_DATA):
        os.makedirs(FOLDER_DATA)
        print(f"Создана папка: {FOLDER_DATA}")
        log_error(f"Создана папка: {FOLDER_DATA}")

        # Применяем полные права ко всем пользователям на созданную папку
        subprocess.run(['icacls', FOLDER_DATA, '/grant', 'Everyone:F', '/T', '/C'], shell=True)
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
                "password": ""
        }
        with open(PATH_DATA_FILE, 'w', encoding='utf-8') as file:
            json.dump(initial_data, file, indent=4)  # Записываем данные в формате JSON с отступами
        print(f"Создан файл: {PATH_DATA_FILE} с начальными данными")
        log_error(f"Создан файл: {PATH_DATA_FILE} с начальными данными")

    # Проверяем, существует ли файл log_chpcgu.txt. Если нет, то создаем его.
    if not os.path.exists(PATH_LOG_FILE):
        with open(PATH_LOG_FILE, 'w', encoding='utf-8') as file:
            file.write("")  # Создаем пустой лог-файл
        print(f"Создан файл: {PATH_LOG_FILE}")
        log_error(f"Создан файл: {PATH_LOG_FILE}")

    # Проверяем, существует ли файл install_info.txt. Если нет, то создаем его.
    if not os.path.exists(PATH_INSTALL_INFO_FILE):
        with open(PATH_INSTALL_INFO_FILE, 'w', encoding='utf-8') as file:
            file.write("")  # Создаем пустой лог-файл
        print(f"Создан файл: {PATH_INSTALL_INFO_FILE}")
        log_error(f"Создан файл: {PATH_INSTALL_INFO_FILE}")

    # Применяем полные права ко всем пользователям на файлы, если они уже существуют или только что были созданы.
    # Задаем доступ для всех на запись чтение изменение.
    subprocess.run(['icacls', FOLDER_DATA, '/grant', 'Everyone:F', '/T', '/C'], shell=True)
    print(f"Права доступа обновлены для папки и вложенных файлов: {FOLDER_DATA}")
    log_error(f"Права доступа обновлены для папки и вложенных файлов: {FOLDER_DATA}")


def check_mode_run_app():
    """Проверяет, запущено ли приложение от имени администратора."""
    try:
        if os.name == 'nt':
            app_is_admin = bool(ctypes.windll.shell32.IsUserAnAdmin())
            return "admin" if app_is_admin else "user"
    except:
        log_error(f"Запуск приложения в режиме ПОЛЬЗОВАТЕДЬ")
    return "user"


# --------------------------Работа с паролем для приложения-------------------
def hash_password(password: str) -> str:
    """Хеширует пароль с использованием HMAC и секретного ключа."""
    hash_psw = hmac.new(SECRET_KEY, password.encode('utf-8'), hashlib.sha256).hexdigest()
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


# -------------------------------------- END ---------------------------------

# -------------------------------- Работа с реестром -------------------------
def set_password_in_registry(password: str):
    """Записывает пароль в реестр."""
    # Путь в реестре - Компьютер-HKEY_LOCAL_MACHINE-SOFTWARE-CPG Password
    key_path = r"Software\CPG Password"

    # Открываем или создаем ключ реестра
    try:
        key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key_path)
        winreg.SetValueEx(key, "Password", 0, winreg.REG_SZ, password)
        winreg.CloseKey(key)
        print("Пароль успешно сохранен в реестр.")
        log_error("Пароль успешно сохранен в реестр.")
    except Exception as e:
        print(f"Ошибка при записи пароля в реестр: {e}")
        log_error(f"{e}")


def get_password_from_registry():
    """Читает пароль из реестра."""
    key_path = r"Software\CPG Password"

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
        log_error(f"{e}")
        return False


def delete_password_from_registry():
    """Удаляет запись пароля из реестра."""
    key_path = r"Software\CPG Password"

    try:
        # Открываем ключ реестра с правами на запись
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, "Password")
        winreg.CloseKey(key)
        print("Пароль удален из реестра.")
        log_error("Пароль удален из реестра.")
    except FileNotFoundError:
        print("Запись не найдена в реестре.")
        log_error("Запись не найдена в реестре.")
    except Exception as e:
        print(f"Ошибка при удалении записи пароля: {e}")
        log_error(f"Ошибка при удалении записи пароля: {e}")

# -------------------------------------- END ---------------------------------
#delete_password_from_registry()