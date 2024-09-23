import json
import os
from datetime import datetime

from config_app import path_data_file, FOLDER_DATA, path_log_file
from function import read_json


def function_to_create_path_data_files():
    """Функция проверки и создания файлов данных для приложения"""

    # Проверяем, существует ли папка. Если нет, то создаем её.
    if not os.path.exists(FOLDER_DATA):
        os.makedirs(FOLDER_DATA)
        print(f"Создана папка: {FOLDER_DATA}")

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
        with open(path_log_file, 'w') as file:
            file.write("")  # Создаем пустой лог-файл
        print(f"Создан файл: {path_log_file}")


def date_control():
    """
    Функция контроля даты.
    """
    # Получаем сегодняшнюю дату
    today = datetime.today().date()

    # Проверяем дату из файла данных
    date_to_datafile = read_json("date")
    username_blocking_to_datafile = read_json("username_blocking")
    remaining_time_to_datafile = read_json("remaining_time")
    # Выводим результат
    print("date_to_datafile:", date_to_datafile)
    print("username_blocking_to_datafile:", username_blocking_to_datafile)
    print("remaining_time_to_datafile:", remaining_time_to_datafile)


if __name__ == '__main__':
    function_to_create_path_data_files()
    date_control()
