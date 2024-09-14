import subprocess
import os
import sys
import ctypes


def is_admin():
    """
    Проверяет, запущен ли скрипт с правами администратора.

    :return: True, если запущен с правами администратора, иначе False.
    """
    try:
        # Проверка административных прав
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin():
    """
    Перезапускает текущий скрипт от имени администратора.
    """
    try:
        # Запуск скрипта от имени администратора
        ctypes.windll.shell32.ShellExecuteW(
                None,
                "runas",
                sys.executable,
                " ".join(sys.argv),
                None,
                0
        )
        print("Скрипт был запущен с правами администратора")
    except Exception as e:
        print(f"Не удалось перезапустить скрипт с правами администратора: {e}")


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

        # Очищаем содержимое файла lock_time.json
        lock_time_file = 'lock_time.json'
        if os.path.exists(lock_time_file):
            with open(lock_time_file, 'w') as file:
                file.write('')  # Записываем пустую строку в файл
            print(f"Содержимое файла {lock_time_file} было стерто.")
        else:
            print(f"Файл {lock_time_file} не найден.")

    except subprocess.CalledProcessError as e:
        print(f"Ошибка при разблокировке пользователя {username}: {e}")


# Проверка и запуск от имени администратора
if __name__ == "__main__":
    if not is_admin():
        print("Скрипт не запущен с правами администратора. Попытка перезапуска...")
        run_as_admin()
    else:
        # Разблокировка пользователя
        unblock_user("test")  # Разблокируем
