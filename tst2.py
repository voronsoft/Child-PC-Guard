# TODO не отрабатывает код выхода на экран блокировки а так же не блокирует пользователя
import ctypes
import os
import subprocess

from function import log_error, is_session_active, read_data_json


def blocking(username, id_ses):
    """
    Функция блокировки пользователя.

    :param username: Имя блокируемого пользователя
    :param id_ses: ID сессии для блокировки экрана рабочего стола
    """
    # Статус запуска программы с привилегиями администратора или нет
    status_run = ctypes.windll.shell32.IsUserAnAdmin()
    log_error(f"0(blocking()) Статус запуска скрипта от имени Администратора: {status_run}")

    # Если запуск происходит от имени администратора
    if status_run:
        # Получаем имя пользователя активной сесии
        usr = os.getlogin()
        log_error(f"1(blocking()) Получаем имя пользователя текущей сессии: {usr}")

        # Получаем имя защищенного пользователя
        protect_usr = read_data_json("protected_user")
        log_error(f"2(blocking()) Получаем имя защищенного пользователя: {protect_usr}")

        # Получаем id активной сессии
        id_ses_active = ctypes.windll.kernel32.WTSGetActiveConsoleSessionId()
        log_error(f"3(blocking()) Получаем id текущей сессии: {id_ses_active}")

        # Если имя защищенного пользователя одинаково с именем блокируемого пользователя
        if protect_usr == usr:
            log_error("5(blocking()) Это сессия защищенного пользователя, команда блокировки ОТМЕНЕНА.")
            return
        # Если имя защищенного пользователя не совпадает с именем блокируемого пользователя
        elif protect_usr != usr:
            # Если сессия активна
            if is_session_active(usr):
                log_error("6(blocking()) Должна отработать блокировка")
                # --------------------------------------------------------------
                # Если id сессии не пустой
                if id_ses is not None:
                    # Команда выхода пользователя из сессии
                    command_logoff = f"logoff {id_ses}"
                    # Команда для блокировки учетной записи пользователя через PowerShell
                    command_disable_user = f'PowerShell -Command "Disable-LocalUser -Name \'{username}\'"'

                    # ------------------ Закрываем пользовательскую сессию -----------------------
                    try:
                        log_error(f"7(blocking()) Учетная запись {username} успешно заблокирована.")
                        # Выполнение команды через subprocess
                        result = subprocess.run(command_disable_user, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    except subprocess.CalledProcessError as e:
                        log_error(f"8(blocking()) Ошибка при выполнении команды блокировки учетки:\n{e.stderr}")
                    # ----------------------------------- END ------------------------------------
                    # ------------------------ Блокируем учетную запись --------------------------
                    try:
                        log_error("9(blocking()) Отработала команда блокировки экрана")
                        # Выполнение команды logoff для указанной сессии
                        subprocess.run(command_logoff, shell=True, check=True)
                    except Exception as e:
                        log_error(f"10(blocking()) Ошибка при выполнении команды выхода на экран блокировки:\n{e}")
                    # ----------------------------------- END ------------------------------------
                else:
                    log_error("11(blocking()) Не удалось получить ID сессии. Команды не будут выполнены.")
                # --------------------------------------------------------------
            # Сессия не активна
            else:
                log_error("12(blocking()) Пользователь не активировал сессию")
                return
    # Если нет прав Администратора на запуск, отмена операции
    else:
        log_error(f"13(blocking()) Отмена блокировки пользователя запущено НЕ от имени Администратора\n")


if __name__ == '__main__':
    usr = os.getlogin()
    id_ses_active = ctypes.windll.kernel32.WTSGetActiveConsoleSessionId()

    blocking(usr, id_ses_active)
