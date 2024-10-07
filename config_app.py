import json
import os
import sys

# Секретный ключ для хеширования пароля
SECRET_KEY = b'super_simple_key_ChilD_Ps_GuuaRD'

# Определяем корневую папку проекта (определяется путем с какого места вызван код из файла)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Получаем имя диска, где установлено приложение (парсим строку)
DISK_LETTER = os.path.splitdrive(PROJECT_ROOT)[0] + "\\"


# ================= Функции формирования динамических путей к приложениям===================
# Возвращает корректный путь к папке с данными, чтобы exe\py -приложение могло найти ресурс.
def resource_path_data(relative_path=""):
    """ Возвращает путь к папке img с изображениями относительно исполняемого файла или скрипта """
    if getattr(sys, 'frozen', False):  # Если приложение запущено как (.exe).
        # Путь к системной папке в Windows
        base_path = os.path.join(os.environ.get('PROGRAMDATA'), "Child PC Guard Data")
    else:  # Если приложение запущено как обычный скрипт (.py).
        # Получаем директорию, где находится .py файл
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)


# Возвращает корректный путь к файлу, чтобы exe\py -приложение могло найти ресурс.
def resource_path(relative_path=""):
    """ Возвращает путь к папке img с изображениями относительно исполняемого файла или скрипта """
    if getattr(sys, 'frozen', False):  # Если приложение запущено как (.exe).
        # Получаем директорию, где находится .exe приложение
        base_path = os.path.dirname(sys.executable)
    else:  # Если приложение запущено как обычный скрипт (.py).
        # Получаем директорию, где находится .py файл
        base_path = os.path.dirname(os.path.abspath(__file__))

    # Возвращаем полный путь к папке img
    return os.path.join(base_path, relative_path)


def read_file(file_path):
    """
    Считывает файл и ищет строку с указанным ключом

    :param file_path str: Путь к файлу
    :return str: Значение или None, если ключ не найден.
    """
    try:
        # Открываем файл для чтения
        with open(file_path, 'r', encoding="utf-8") as file:
            file_path = file.read()  # Считываем содержимое файла
        # Если ключ не найден, возвращаем None
        return file_path.strip()
    except Exception as e:
        print(f"(rf1)Ошибка:\n{file_path}")
        return None


# Возвращает корректный путь к папке установки приложения, чтобы exe\py -приложение могло найти ресурс.
def resource_path_inst_app():
    """ Возвращает путь к папке установки программы относительно исполняемого файла или скрипта """
    try:
        print(1)
        if getattr(sys, 'frozen', False):  # Если приложение запущено как (.exe).
            print(2)
            # Считываем данные по пути из файла системы - (X):\DataProgram\install_info.txt
            app_inst_base_path = read_file(os.path.join(FOLDER_DATA, "install_info.txt"))

            print("2-1  ", FOLDER_DATA)
            print("2-2  ", os.path.join(FOLDER_DATA, "install_info.txt"))
            print("2-3  ", app_inst_base_path)
        else:  # Если приложение запущено как обычный скрипт (.py).
            # Считываем данные по пути из директории проекта
            print(3)
            app_inst_base_path = read_file(os.path.join(FOLDER_DATA, "install_info.txt"))

            print("3-1 ", FOLDER_DATA)
            print("3-2 ", os.path.join(FOLDER_DATA, "install_info.txt"))
            print("3-3 ", app_inst_base_path)

        # Возвращаем полный путь к папке img
        return os.path.join(app_inst_base_path)

    except Exception as e:
        print("1 ошибка: ", e)


# ========================================== END ===========================================
# Определяем путь к папке данных для приложения
FOLDER_DATA = resource_path_data()
# Определяем путь к папке с изображениями
FOLDER_IMG = resource_path("img")
# Определяем путь к папке установки приложения
FOLDER_INSTALL_APP = resource_path_inst_app()
# Путь к главному изображению программы на заставку
SCREENSAVER1 = os.path.join(FOLDER_IMG, "screensaver1.png")
SCREENSAVER2 = os.path.join(FOLDER_IMG, "screensaver2.png")
# Путь к файлу данных - data.json
PATH_DATA_FILE = os.path.join(FOLDER_DATA, "data.json")
# Путь к файлу логов - log_chpcgu.txt
PATH_LOG_FILE = os.path.join(FOLDER_DATA, "log_chpcgu.txt")
# Путь к файлу с информацией о пути установки приложения - install_info.txt
PATH_INSTALL_INFO_FILE = os.path.join(FOLDER_DATA, "install_info.txt")

# =================================== Путь к приложениям ==================================
path_main_app = os.path.join(FOLDER_INSTALL_APP, "Child PC Guard.exe")  # Путь к главному приложению
path_timer_exe = os.path.join(FOLDER_INSTALL_APP, "Child PC Timer.exe")  # Путь к приложению Таймер
path_monitor_exe = os.path.join(FOLDER_INSTALL_APP, "Windows CPG Monitor.exe")  # Путь к приложению Монитор
path_unblock_usr_exe = os.path.join(FOLDER_INSTALL_APP, "Child PC Unlock User.exe")  # Путь к приложению Разблокировки
path_bot_tg_exe = os.path.join(FOLDER_INSTALL_APP, "run_bot_telegram.exe.")  # Путь к приложению Бота
# ========================================== END ==========================================


if __name__ == "__main__":
    ...
print("PROJECT_ROOT: ", PROJECT_ROOT)
print("DISK_LETTER: ", DISK_LETTER)
print("FOLDER_DATA: ", FOLDER_DATA)
print("FOLDER_IMG: ", FOLDER_IMG)
print("FOLDER_INSTALL_APP: ", FOLDER_INSTALL_APP)
print("SCREENSAVER1: ", SCREENSAVER1)
print("SCREENSAVER2: ", SCREENSAVER2)
print("PATH_DATA_FILE: ", PATH_DATA_FILE)
print("PATH_LOG_FILE: ", PATH_LOG_FILE)
print("PATH_INSTALL_INFO_FILE: ", PATH_INSTALL_INFO_FILE)

print("===============================app exe===================================")
print("path_timer_exe: ", path_timer_exe)
print("path_monitor_exe", path_monitor_exe)
print("path_unblock_usr_exe", path_unblock_usr_exe)
print("path_main_app", path_main_app)
print("path_bot_tg_exe", path_bot_tg_exe)
print("===============================app exe===================================")
