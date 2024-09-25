import os
import sys
import time
import stat  # Импортируем модуль для управления правами доступа к файлам
import json
import ctypes
import subprocess

from datetime import datetime

from config_app import FOLDER_DATA, path_data_file, path_log_file


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
                    0  # 1-отобразить консоль \ 0-скрыть консоль
            )
            sys.exit()  # Завершаем текущий процесс, чтобы предотвратить двойной запуск
        except Exception as e:
            ctypes.windll.user32.MessageBoxW(
                    None,
                    f"Не удалось запустить программу с правами администратора:\n\n{e}",
                    "Ошибка",
                    1
            )


def read_json(key, file_path=path_data_file):
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
        print(f"Файл {file_path} не найден.")
        return None
    except json.JSONDecodeError:
        print("Ошибка чтения JSON-файла.")
        return None
    except KeyError:
        print(f"Ключ '{key}' не найден в JSON-файле.")
        return None


def update_json(key, value, file_path=path_data_file):
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
        print(f"Файл {file_path} не найден.")
    except json.JSONDecodeError:
        print("Ошибка чтения JSON-файла.")
    except KeyError:
        print(f"Ключ '{key}' не найден в JSON-файле.")
    except Exception as e:
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
        print(f"Получение данных сессии по имени пользователя\nОшибка при выполнении команды:\n{e}")
    except Exception as e:
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
            # TODO закомментированная команда для теста
            # Выполнение команды logoff для указанной сессии
            subprocess.run(command_logoff, shell=True, check=True)
            print("1 Отработала команда блокировки экрана")
            time.sleep(1)
            # TODO закомментированная команда для теста
            # Выполняем команду для блокировки учетной записи
            # subprocess.run(command_disable_user, shell=True, check=True)
            print("2 Отработала команда блокировки учетной записи")
            print(f"Учетка заблокирована {username} (ID: {id_ses_user}).")
        except subprocess.CalledProcessError as e:
            print(f"Ошибка при выполнении команд: {e}")
            time.sleep(3)
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
        print(f"Пользователь {username} разблокирован.")
        return True
    except Exception as e:
        print(f"Ошибка при разблокировке пользователя {username}: {e}")

        ctypes.windll.user32.MessageBoxW(
                None,
                f"Ошибка при разблокировке пользователя - {username}:\n\n{e}",
                "Ошибка",
                1
        )
        return False

def username_session():
    """Получение имени пользователя в сессии"""
    username_session = os.getlogin()  # Получение имени текущего пользователя
    return username_session


def show_message(username, time):
    """
    Показывает сообщение о предстоящей блокировке.

    :param username: Имя пользователя для отображения в сообщении.
    """
    username_session = os.getlogin()
    if username != username_session:
        ctypes.windll.user32.MessageBoxW(
                None,
                f"У вас есть - {time} секунд(ы).\nПо истечении этого времени вы будете заблокированы.",
                "Автоматическое закрытие",
                0
        )
    if username == username_session:
        ctypes.windll.user32.MessageBoxW(
                None,
                "Блокировка отключена.\nВы не можете блокировать самого себя.\n\nПрограмма будет закрыта.",
                "Автоматическое закрытие",
                0
        )


def auto_close():
    """
    Автоматически закрывает окно сообщения через 5 секунд.
    """
    time.sleep(5)
    hwnd = ctypes.windll.user32.FindWindowW(None, "Автоматическое закрытие")
    if hwnd:
        ctypes.windll.user32.PostMessageW(hwnd, 0x0010, 0, 0)  # 0x0010 — это WM_CLOSE, команда закрытия окна.


# TODO дописать функцию
def date_control():
    """
    Функция контроля даты.
    """
    # Получаем сегодняшнюю дату
    today = datetime.today().date()

    # Проверяем дату из файла данных

    #
    #
    #

    # Выводим результат
    print("Сегодняшняя дата:", today)


def function_to_create_path_data_files():
    """Функция проверки и создания файлов данных для приложения"""

    # Проверяем, существует ли папка. Если нет, то создаем её.
    if not os.path.exists(FOLDER_DATA):
        os.makedirs(FOLDER_DATA)
        print(f"Создана папка: {FOLDER_DATA}")
        # Изменяем права доступа к папке, чтобы все пользователи могли читать, писать и выполнять файлы
        os.chmod(FOLDER_DATA, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        # S_IRWXU - полный доступ для владельца (User)
        # S_IRWXG - полный доступ для группы (Group)
        # S_IRWXO - полный доступ для других (Others)
        print(f"Установлены полные права доступа к папке: {FOLDER_DATA}")

    # Проверяем, существует ли файл data.json. Если нет, то создаем его и записываем начальные данные.
    if not os.path.exists(path_data_file):
        initial_data = {
                "username_blocking": "",
                "remaining_time": 0,
                "date": "0001-02-03"
        }
        with open(path_data_file, 'w', encoding='utf-8') as file:
            json.dump(initial_data, file, indent=4)  # Записываем данные в формате JSON с отступами
        print(f"Создан файл: {path_data_file} с начальными данными")
        # Устанавливаем полный доступ к файлу для всех пользователей
        os.chmod(path_data_file, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        print(f"Установлены полные права доступа к файлу: {path_data_file}")

    # Проверяем, существует ли файл log_chpcgu.txt. Если нет, то создаем его.
    if not os.path.exists(path_log_file):
        with open(path_log_file, 'w', encoding='utf-8') as file:
            file.write("")  # Создаем пустой лог-файл
        print(f"Создан файл: {path_log_file}")
        # Устанавливаем полный доступ к файлу для всех пользователей
        os.chmod(path_log_file, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        print(f"Установлены полные права доступа к файлу: {path_log_file}")
