import ctypes
import json
import subprocess
import time
import os
import sys

# Путь к файлу для хранения оставшегося времени до блокировки и счетчика завершений
REMAINING_TIME_FILE = "file_remaining_time.txt"
USR_BLCK = "file_username_blocking.txt"


def is_admin():
    """
    Проверяет, запущен ли скрипт с правами администратора.
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin():
    """
    Проверяет, запущено ли приложение с правами администратора.
    Если нет, перезапускает его с запросом прав администратора.
    """
    try:
        # Проверяем, запущено ли приложение с правами администратора
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    except:
        is_admin = False

    if not is_admin:
        # Если приложение запущено без прав администратора, перезапускаем его с запросом прав администратора
        try:
            ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", sys.executable, ' '.join([f'"{arg}"' for arg in sys.argv]), None, 1
            )
            sys.exit()  # Завершаем текущий процесс, чтобы предотвратить двойной запуск
        except Exception as e:
            print("Ошибка ", e)
            ctypes.windll.user32.MessageBoxW(
                    None,
                    f"Не удалось запустить программу с правами администратора:\n\n{e}",
                    "Ошибка",
                    0
            )

            # wx.MessageBox(f"Не удалось запустить программу с правами администратора: {e}", "Ошибка", wx.ICON_ERROR)
            # sys.exit(3)


def save_username_blocking(username):
    """
    Запись имени пользователя для которого выбрана блокировка
    :param username: Имя пользователя для блокировки.
    """
    with open(USR_BLCK, "w") as file:
        file.write(str(username))


def load_username_blocking():
    """
    Загружает имя пользователя из файла.
    """
    if os.path.exists(USR_BLCK):
        with open(USR_BLCK, "r") as file:
            temp = file.read().strip()
            return str(temp)
    return None


def delete_username_blocking_file():
    """
    Удаляет файл, содержащий имя пользователя для блокировки.
    """
    if os.path.exists(USR_BLCK):
        os.remove(USR_BLCK)


def save_remaining_time(remaining_time):
    """
    Сохраняет оставшееся время до блокировки в файл.
    :param remaining_time: Остаток времени в секундах.
    """
    with open(REMAINING_TIME_FILE, "w") as file:
        file.write(str(remaining_time))


def load_remaining_time():
    """
    Загружает оставшееся время до блокировки из файла.
    :return: Остаток времени в секундах или None, если файл не существует.
    """
    try:
        if os.path.exists(REMAINING_TIME_FILE):
            with open(REMAINING_TIME_FILE, "r", encoding="utf-8") as file:
                temp = file.read().strip()
                if temp == "":
                    return 0
                return int(temp)

        return None
    except Exception as e:
        print("Ошибка: ", e)


def delete_remaining_time_file():
    """
    Удаляет файл, содержащий остаток времени до блокировки.
    """
    if os.path.exists(REMAINING_TIME_FILE):
        os.remove(REMAINING_TIME_FILE)


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
        print(f"Ошибка при выполнении команды: {e}")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
    return None


def blocking(username, id_ses_user):
    """
    Функция блокировки пользователя.

    :param username: Имя блокируемого пользователя
    :param id_sess_user: ID сессии для блокировки экрана рабочего стола
    """
    # command1 = f'net user "{username}" /active:no'
    # subprocess.run(command1, shell=True, check=True)
    # print("Выполняем команду в командной строке для блокировки учетной записи")
    #
    # time.sleep(1)

    # command2 = 'C:\\Windows\\System32\\rundll32.exe user32.dll,LockWorkStation'
    # subprocess.run(command2, shell=True, check=True)
    # print("Выполнение команды блокировки рабочего стола (экран блокировки)")
    if id_ses_user is not None:
        command_logoff = f"logoff {id_ses_user}"
        command_disable_user = f'net user "{username}" /active:no'
        try:
            # Выполнение команды logoff для указанной сессии
            subprocess.run(command_logoff, shell=True, check=True)
            print("1 Отработала команда блокировки экрана")
            time.sleep(3)
            # TODO закоментированная команда для теста
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
        username_session = os.getlogin()  # Получение имени текущего пользователя
        if username != username_session and username != "":
            # Формируем команду для разблокировки пользователя
            command = f'net user "{username}" /active:yes'
            # Выполняем команду в командной строке
            subprocess.run(command, shell=True, check=True)
            print(f"Пользователь {username} разблокирован.")
            time.sleep(1)

            # Очищаем содержимое файла file_remaining_time.txt
            if os.path.exists(REMAINING_TIME_FILE):
                with open(REMAINING_TIME_FILE, 'w') as file:
                    file.write('')  # Записываем пустую строку в файл
                print(f"Содержимое файла {REMAINING_TIME_FILE} было стерто.")
                time.sleep(1)
            else:
                print(f"Файл {REMAINING_TIME_FILE} не найден.")

            # Очищаем содержимое файла file_username_blocking.txt
            if os.path.exists(USR_BLCK):
                with open(USR_BLCK, 'w') as file:
                    file.write('')  # Записываем пустую строку в файл
                print(f"Содержимое файла {USR_BLCK} было стерто.")
                time.sleep(1)
            else:
                print(f"Файл {REMAINING_TIME_FILE} не найден.")

    except subprocess.CalledProcessError as e:
        print(f"Ошибка при разблокировке пользователя {username}: {e}")


def username_session():
    """Получение имени пользователя в сесии"""
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
