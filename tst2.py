import ctypes
import os
import subprocess

from function import log_error, read_data_json, show_message_with_auto_close


def blocking_v2(username):
    """
    Функция блокировки пользователя. Для windows 10/11 HOME

    :param username: Имя блокируемого пользователя
    """
    # Статус запуска программы с привилегиями администратора или нет
    status_run = ctypes.windll.shell32.IsUserAnAdmin()
    log_error(f"0(blocking_v2()) Статус запуска скрипта от имени Администратора: {status_run}")

    # Если запуск происходит от имени администратора
    if status_run:
        # Получаем имя пользователя активной сесии
        usr_ses = os.getlogin()
        log_error(f"1(blocking_v2()) Получаем имя пользователя текущей сессии: {usr_ses}")

        # Получаем имя защищенного пользователя
        protect_usr = read_data_json("protected_user")
        log_error(f"2(blocking_v2()) Получаем имя защищенного пользователя: {protect_usr}")

        # Если имя защищенного пользователя одинаково с именем пользователя активной сессии
        if protect_usr == usr_ses:
            log_error("5(blocking_v2()) Это сессия защищенного пользователя, команда блокировки ОТМЕНЕНА.")
            # Открытие окна с сообщением
            ctypes.windll.user32.MessageBoxW(0, "Это сессия защищенного пользователя, команда блокировки ОТМЕНЕНА.",
                                             "Отмена операции", 0)

            return
        # Если имя защищенного пользователя не совпадает с именем блокируемого пользователя
        elif protect_usr != usr_ses:
            log_error("6(blocking_v2()) Должна отработать блокировка")
            # Команда выхода пользователя из сессии
            command_logoff = f"logoff"
            # Команда для блокировки учетной записи пользователя через PowerShell
            command_disable_user = f'PowerShell -Command "Disable-LocalUser -Name \'{username}\'"'

            # ------------------ Закрываем пользовательскую сессию -----------------------
            try:
                log_error(f"7(blocking_v2()) Учетная запись {username} успешно заблокирована.")
                # Выполнение команды через subprocess
                result = subprocess.run(command_disable_user, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            except subprocess.CalledProcessError as e:
                log_error(f"8(blocking_v2()) Ошибка при выполнении команды блокировки учетки:\n{e.stderr}")
            # ----------------------------------- END ------------------------------------
            # ------------------------ Блокируем учетную запись --------------------------
            try:
                log_error("9(blocking_v2()) Отработала команда блокировки экрана")
                # Выполнение команды logoff для указанной сессии
                subprocess.run(command_logoff, shell=True, check=True)
            except Exception as e:
                log_error(f"10(blocking_v2()) Ошибка при выполнении команды выхода на экран блокировки:\n{e}")
                # ----------------------------------- END ------------------------------------
    # Если нет прав Администратора на запуск, отмена операции
    else:
        log_error(f"13(blocking_v2()) Отмена блокировки пользователя запущено НЕ от имени Администратора\n")


if __name__ == '__main__':
    username = "test"
    blocking_v2(username)
