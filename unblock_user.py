import ctypes
import subprocess

from test_block import is_admin, run_as_admin, read_json, update_json

USERNAME = read_json('username_blocking')

def unblock_user(username):
    """
    Разблокирует учетную запись пользователя Windows.

    :param username: Имя учетной записи пользователя для разблокировки.
    """
    try:

        if len(username) > 3:
            # Формируем команду для разблокировки пользователя
            command = f'net user "{username}" /active:yes'
            # Выполняем команду в командной строке
            subprocess.run(command, shell=True, check=True)
            print(f"Пользователь {username} разблокирован.")

            # Очищаем время в файле с данными.
            update_json("remaining_time", 0)

    except Exception as e:
        print(f"Ошибка при разблокировке пользователя {username}: {e}")


# Проверка и запуск от имени администратора
if __name__ == "__main__":
    if not is_admin():
        ctypes.windll.user32.MessageBoxW(
                None,
                f"Скрипт запущен без правами администратора.\nПопытка перезапуска...",
                "Ошибка",
                1
        )

        print("Скрипт запущен без правами администратора.\nПопытка перезапуска...")
        run_as_admin()
    else:
        # Разблокировка пользователя
        # получаем имя пользователя из файла с данными
        user = read_json("username_blocking")
        unblock_user(USERNAME)  # Разблокируем
