import os
import sys
import time

# Определяем корневую папку проекта
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Получаем имя диска (вид С:\)
DISK_LETTER = os.path.splitdrive(PROJECT_ROOT)[0] + "\\"

# Путь к папке с данными
FOLDER_DATA = os.path.join(DISK_LETTER, "ProgramData", "Child PC Guard Data")

# # =============================== Путь к папке с изображениями =============================
# # Возвращает правильный путь к файлу, чтобы exe-приложение могло найти ресурс.
# # Если приложение запущено в виде exe, sys._MEIPASS указывает на временную папку, где хранятся все распакованные файлы.
# # Если приложение запущено как Python-скрипт, путь строится относительно текущего каталога.
# try:
#     # Если приложение запущено как exe, _MEIPASS указывает на временную папку
#     FOLDER_IMG = os.path.join(sys._MEIPASS, "img")
#     # print("exe_path_run", FOLDER_IMG)
#
# except AttributeError:
#     # Если запущено как обычный скрипт, используем текущий каталог
#     FOLDER_IMG = os.path.join(os.path.abspath("."), "img")
#     # print("py_path_run", FOLDER_IMG)
# # ========================================== END ==========================================
# =============================== Путь к папке с изображениями =============================
# Возвращает правильный путь к файлу, чтобы exe-приложение могло найти ресурс.
def resource_path(relative_path):
    """ Возвращает путь к папке img с изображениями относительно исполняемого файла или скрипта """
    if getattr(sys, 'frozen', False):
        # Если приложение запущено как .exe
        # Получаем директорию, где находится .exe
        base_path = os.path.dirname(sys.executable)
    else:
        # Если приложение запущено как обычный скрипт .py
        # Получаем директорию, где находится .py файл
        base_path = os.path.dirname(os.path.abspath(__file__))

    # Возвращаем полный путь к папке img
    return os.path.join(base_path, "img")


# Определяем путь к папке с изображениями
FOLDER_IMG = resource_path("img")

# Для проверки пути (можно раскомментировать при необходимости)
print("Path to images folder:", FOLDER_IMG)
# ========================================== END ==========================================

# Путь к папке с изображениями
# FOLDER_IMG = os.path.join(DISK_LETTER, "Program Files (x86)", "Child PC Guard", "img")

# Путь к главному изображению программы на заставку
SCREENSAVER1 = os.path.join(FOLDER_IMG, "screensaver1.png")
SCREENSAVER2 = os.path.join(FOLDER_IMG, "screensaver2.png")

# Путь к файлу данных - data.json
path_data_file = os.path.join(FOLDER_DATA, "data.json")

# Путь к файлу логов - log_chpcgu.txt
path_log_file = os.path.join(FOLDER_DATA, "log_chpcgu.txt")

# Путь к приложениям Блокировщик, Таймер, Монитор, Разблокировать
path_timer_exe = os.path.join(DISK_LETTER, "Program Files (x86)", "Child PC Guard", "Child PC Timer.exe")
path_monitor_exe = os.path.join(DISK_LETTER, "Program Files (x86)", "Child PC Guard", "Windows CPG Monitor.exe")
path_unblock_usr_exe = os.path.join(DISK_LETTER, "Program Files (x86)", "Child PC Guard", "Child PC Unlock User.exe")
# Путь к главному приложению
path_main_app = os.path.join(DISK_LETTER, "Program Files (x86)", "Child PC Guard", "Child PC Guard.exe")




if __name__ == "__main__":
    print("PROJECT_ROOT", PROJECT_ROOT)
    print("DISK_LETTER", DISK_LETTER)
    print("FOLDER_DATA", FOLDER_DATA)
    print("FOLDER_IMG", FOLDER_IMG)
    print("path_data_file", path_data_file)
    print("path_log_file", path_log_file)
    print("SCREENSAVER1", SCREENSAVER1)