import os
import json
import subprocess

# Определяем корневую папку проекта
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Получаем имя диска (вид С:\)
DISK_LETTER = os.path.splitdrive(PROJECT_ROOT)[0] + "\\"

# Путь к папке с данными
FOLDER_DATA = os.path.join(DISK_LETTER, "ProgramData", "Child PC Guard Data2")

path_data_file = os.path.join(FOLDER_DATA, 'data.json')  # Путь к файлу данных
path_log_file = os.path.join(FOLDER_DATA, 'log_chpcgu.txt')  # Путь к лог-файлу

def function_to_create_path_data_files():
    """Функция проверки и создания файлов данных для приложения с установкой прав доступа"""

    # Проверяем, существует ли папка. Если нет, то создаем её.
    if not os.path.exists(FOLDER_DATA):
        os.makedirs(FOLDER_DATA)  # Создаем папку
        print(f"Создана папка: {FOLDER_DATA}")

        # Применяем полные права ко всем пользователям на созданную папку
        subprocess.run(['icacls', FOLDER_DATA, '/grant', 'Everyone:F', '/T', '/C'], shell=True)
        # /grant - предоставить права
        # Everyone:F - разрешить полные права для всех пользователей
        # /T - рекурсивно для всех вложенных файлов и папок
        # /C - продолжить выполнение даже при ошибках
        print(f"Права доступа установлены для папки: {FOLDER_DATA}")

    # Проверяем, существует ли файл data.json. Если нет, то создаем его и записываем начальные данные.
    if not os.path.exists(path_data_file):
        initial_data = {
            "username_blocking": "",
            "remaining_time": 0,
            "date": "0001-02-03"
        }
        with open(path_data_file, 'w') as file:
            json.dump(initial_data, file, indent=4)  # Записываем данные в формате JSON с отступами
        print(f"Создан файл: {path_data_file} с начальными данными")

    # Проверяем, существует ли файл log_chpcgu.txt. Если нет, то создаем его.
    if not os.path.exists(path_log_file):
        with open(path_log_file, 'w', encoding="utf-8") as file:
            file.write("")  # Создаем пустой лог-файл
        print(f"Создан файл: {path_log_file}")

    # Применяем полные права ко всем пользователям на файлы, если они уже существуют или только что были созданы.
    subprocess.run(['icacls', FOLDER_DATA, '/grant', 'Everyone:F', '/T', '/C'], shell=True)
    print(f"Права доступа обновлены для папки и всех вложенных файлов: {FOLDER_DATA}")


def write_data_to_files(new_data, log_message):
    """
    Функция для записи данных в файлы data.json и log_chpcgu.txt

    :param new_data: Словарь с данными для записи в data.json
    :param log_message: Сообщение для добавления в log_chpcgu.txt
    """

    # Проверка существования файла data.json и запись данных
    if os.path.exists(path_data_file):
        with open(path_data_file, 'r+', encoding="utf-8") as file:
            # Чтение существующих данных
            current_data = json.load(file)
            # Обновление данными, переданными в функцию
            current_data.update(new_data)
            # Перемотка указателя файла в начало для перезаписи
            file.seek(0)
            json.dump(current_data, file, indent=4)
            # Обрезаем файл, если новые данные меньше старых
            file.truncate()
        print(f"Данные обновлены в файле: {path_data_file}")

    # Проверка существования файла log_chpcgu.txt и запись в лог
    if os.path.exists(path_log_file):
        with open(path_log_file, 'a', encoding="utf-8") as file:
            file.write(log_message + '\n')  # Добавляем сообщение в лог с новой строки
        print(f"Сообщение добавлено в лог: {path_log_file}")





if __name__ == '__main__':
    function_to_create_path_data_files()
    test_data = {
            "username_blocking": "test_user",
            "remaining_time": 120,
            "date": "2024-09-27"
    }

    test_log_message = "Запись в лог 27.09.2024: данные обновлены."

    write_data_to_files(test_data, test_log_message)