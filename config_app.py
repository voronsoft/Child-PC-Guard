import os

# Определяем корневую папку проекта
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Получаем имя диска (вид С:\)
DISK_LETTER = os.path.splitdrive(PROJECT_ROOT)[0] + "\\"

# Путь к папке с данными
FOLDER_DATA = os.path.join(DISK_LETTER, "ProgramData", "Child PC Guard Data")

# Путь к папке с изображениями
FOLDER_IMG = os.path.join("img")

# Путь к главному изображению программы на заставку
SCREENSAVER1 = os.path.join("img", "screensaver1.png")
SCREENSAVER2 = os.path.join("img", "screensaver2.png")

# Путь к файлу данных - data.json
path_data_file = os.path.join(FOLDER_DATA, "data.json")

# Путь к файлу логов - log_chpcgu.txt
path_log_file = os.path.join(FOLDER_DATA, "log_chpcgu.txt")




if __name__ == "__main__":
    print("PROJECT_ROOT", PROJECT_ROOT)
    print("DISK_LETTER", DISK_LETTER)
    print("FOLDER_DATA", FOLDER_DATA)
    print("FOLDER_IMG", FOLDER_IMG)
    print("path_data_file", path_data_file)
    print("path_log_file", path_log_file)