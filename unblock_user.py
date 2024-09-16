import ctypes
import subprocess

from function import is_admin, run_as_admin, read_json, update_json

USERNAME = read_json('username_blocking')
TIME = read_json('remaining_time')

def unblock_user(username):
    """
    Разблокирует учетную запись пользователя Windows.

    :param username: Имя учетной записи пользователя для разблокировки.
    """
    try:

        if len(username) >= 3:
            # Формируем команду для разблокировки пользователя
            command = f'net user "{username}" /active:yes'
            # Выполняем команду в командной строке
            subprocess.run(command, shell=True, check=True)

            # Выводим сообщение
            ctypes.windll.user32.MessageBoxW(
                    None,
                    f"Пользователь {username} разблокирован.",
                    "Успешно",
                    0
            )
            # Очищаем время и имя пользователя в файле с данными.
            update_json('remaining_time', 0)
            update_json('username_blocking', "")
        else:
            # Выводим сообщение
            ctypes.windll.user32.MessageBoxW(
                    None,
                    f"Не удалось разблокировать пользователя - {username}",
                    "ОШИБКА",
                    0
            )

    except Exception as e:
        print(f"Ошибка при разблокировке пользователя {username}: {e}")


# Проверка и запуск от имени администратора
if __name__ == "__main__":
    if USERNAME:
        if not is_admin():
            ctypes.windll.user32.MessageBoxW(
                    None,
                    f"Скрипт запущен без прав администратора.\nПопытка перезапуска...",
                    "Ошибка",
                    0
            )

            # Перезапускаем
            run_as_admin()
        else:
            # Разблокировка пользователя
            unblock_user(USERNAME)  # Разблокируем
    else:
        # Выводим сообщение
        ctypes.windll.user32.MessageBoxW(
                None,
                f"Ни один из пользователей не заблокирован.",
                "ВНИМАНИЕ",
                0
        )

