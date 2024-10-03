import json
import os
import sys
import time

# Определяем корневую папку проекта (определяется путем с какого места вызван код из файла)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Получаем имя диска, где установлено приложение (парсим строку)
DISK_LETTER = os.path.splitdrive(PROJECT_ROOT)[0] + "\\"

# TODO Путь к папке с данными
FOLDER_DATA = os.path.join(os.environ.get('PROGRAMDATA'), "Child PC Guard Data")


# =============================== Путь к папке с изображениями =============================
# Возвращает правильный путь к файлу, чтобы exe-приложение могло найти ресурс.
def resource_path(relative_path=""):
    """ Возвращает путь к папке img с изображениями относительно исполняемого файла или скрипта """
    if getattr(sys, 'frozen', False):
        # Если приложение запущено как (.exe).
        # Получаем директорию, где находится .exe приложение
        base_path = os.path.dirname(sys.executable)
    else:
        # Если приложение запущено как обычный скрипт (.py).
        # Получаем директорию, где находится .py файл
        base_path = os.path.dirname(os.path.abspath(__file__))

    # Возвращаем полный путь к папке img
    return os.path.join(base_path, relative_path)


# Определяем путь к папке с изображениями
FOLDER_IMG = resource_path("img")


# ========================================== END ===========================================


# ======================== Путь к папке с установленным приложением ========================
def read_json(key, file_path):
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
    except Exception as e:
        print("file_path: ", file_path)
        print(f"123Путь установки приложения не считан из файла\n{e}")
        return None


def resource_path_inst_app():
    """ Возвращает путь к папке установки программы относительно исполняемого файла или скрипта """
    if getattr(sys, 'frozen', False):  # Если приложение запущено как (.exe).
        # Считываем данные по пути из файла системы - (X):\DataProgram\install_info.json
        app_inst_base_path = read_json("app_ins_path", os.path.join(FOLDER_DATA, "install_info.json"))
    else:  # Если приложение запущено как обычный скрипт (.py).
        # Считываем данные по пути из директории проекта
        app_inst_base_path = read_json("app_ins_path",
                                       os.path.dirname(os.path.abspath(__file__)) + "\\" + "install_info.json"
                                       )

    # Возвращаем полный путь к папке img
    return os.path.join(app_inst_base_path)


# Определяем путь к папке установки приложения
FOLDER_INSTALL_APP = resource_path_inst_app()
# ========================================== END ===========================================


# Путь к главному изображению программы на заставку
SCREENSAVER1 = os.path.join(FOLDER_IMG, "screensaver1.png")
SCREENSAVER2 = os.path.join(FOLDER_IMG, "screensaver2.png")
# Путь к файлу данных - data.json
path_data_file = os.path.join(FOLDER_DATA, "data.json")
# Путь к файлу логов - log_chpcgu.txt
path_log_file = os.path.join(FOLDER_DATA, "log_chpcgu.txt")
# Путь к файлу с информацией о пути установки приложения - install_info.json
path_install_info_file = os.path.join(FOLDER_DATA, "install_info.json")

# =================================== Путь к приложениям ==================================
# TODO Путь к приложениям Блокировщик, Таймер, Монитор, Разблокировать
path_main_app = os.path.join(FOLDER_INSTALL_APP, "Child PC Guard.exe")  # Путь к главному приложению
path_timer_exe = os.path.join(FOLDER_INSTALL_APP, "Child PC Timer.exe")  # Путь к таймеру
path_monitor_exe = os.path.join(FOLDER_INSTALL_APP, "Windows CPG Monitor.exe")  # Путь к Монитору
path_unblock_usr_exe = os.path.join(FOLDER_INSTALL_APP, "Child PC Unlock User.exe")  # Путь к разблокировке
# ========================================== END ==========================================


if __name__ == "__main__":
    print("FOLDER_INSTALL_APP: ", FOLDER_INSTALL_APP)
    print("PROJECT_ROOT: ", PROJECT_ROOT)
    print("DISK_LETTER: ", DISK_LETTER)
    print("FOLDER_DATA: ", FOLDER_DATA)
    print("FOLDER_INSTALL_APP: ", FOLDER_INSTALL_APP)
    print("FOLDER_IMG: ", FOLDER_IMG)
    print("path_data_file: ", path_data_file)
    print("path_log_file: ", path_log_file)
    print("path_install_info_file: ", path_install_info_file)
    print("SCREENSAVER1: ", SCREENSAVER1)
    print("SCREENSAVER2: ", SCREENSAVER2)
    print("==================================================================")
    print("path_timer_exe: ", path_timer_exe)
    print("path_monitor_exe", path_monitor_exe)
    print("path_unblock_usr_exe", path_unblock_usr_exe)
    print("path_main_app", path_main_app)
    print("==================================================================")

    # time.sleep(140)
