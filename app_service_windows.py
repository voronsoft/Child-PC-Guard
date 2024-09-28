# Код службы WindowsCPGmonitorService (windows 10\11)
# Выполняет: запуск программы Windows CPG APP Monitor.exe и логирование ее работы в лог файл.

import os
import time
import win32event
import subprocess
import win32service
import servicemanager
import win32serviceutil


class SimpleService(win32serviceutil.ServiceFramework):
    """Класс службы для приложения - Child PC Guard.exe (Windows10/11)"""
    # Определение метаданных службы
    _svc_name_ = "WindowsCPGmonitorService"  # Уникальное имя службы (БЕЗ ПРОБЕЛОВ!!!)
    _svc_display_name_ = "Windows CPG Monitor Service"  # Отображаемое имя службы
    # Описание службы
    _svc_description_ = ("Служба мониторинга и запуска промежуточного приложения Windows CPG APP Monitor "
                         "(для работы программы Child PC Guard.)")

    def __init__(self, args):
        # Инициализация службы
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)  # Создание события для остановки службы
        self.running = True  # Флаг для работы службы
        self.process = None  # Переменная для хранения объекта процесса
        self._log_file_path = r"C:\ProgramData\Child PC Guard Data\log_chpcgu.txt"  # Путь к лог-файлу
        self._exe_path = r"C:\Program Files (x86)\Child PC Guard\Windows CPG APP Monitor.exe"  # Путь к испол файлу

    def SvcStop(self):
        """Метод для остановки службы"""
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)  # Уведомление о начале остановки
        win32event.SetEvent(self.stop_event)  # Сигнализируем о том, что служба должна остановиться
        self.running = False  # Изменяем флаг работы службы на False

        if self.process:  # Если процесс запущен
            self.process.terminate()  # Завершаем процесс
            self.save_log_file("Служба ОСТАНОВЛЕНА: 'WindowsCPGmonitorService'")
            self.process = None  # Обнуляем переменную процесса

    def SvcDoRun(self):
        """Метод, вызываемый при запуске службы"""
        try:
            # Логирование запуска службы
            servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                                  servicemanager.PYS_SERVICE_STARTED,
                                  (self._svc_name_, '')
                                  )
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)  # Уведомление о том, что служба запущена
            self.save_log_file("Служба ЗАПУЩЕНА: 'WindowsCPGmonitorService'")
            self.main()  # Переход к основному методу службы
        except Exception as e:
            # Логирование ошибок
            self.save_log_file(f"Ошибка ЗАПУСКА службы: 'WindowsCPGmonitorService'\n{str(e)}")
            servicemanager.LogErrorMsg(f"Ошибка ЗАПУСКА службы: 'WindowsCPGmonitorService'\n{str(e)}")
            raise

    def main(self):
        """Основной метод службы, выполняющий ее логику"""
        while self.running:  # Цикл, работающий пока служба активна
            # Проверяем, запущена ли программа, если нет - запускаем
            if self.process is None or self.process.poll() is not None:
                if os.path.exists(self._exe_path):  # Проверяем, существует ли файл
                    try:
                        # Запись в лог о запуске программы
                        self.save_log_file("ЗАПУСКАЕМ приложение - 'Windows CPG APP Monitor'...")
                        self.process = subprocess.Popen(self._exe_path)  # Запускаем программу
                        self.save_log_file("УСПЕШНО приложение работает - 'Windows CPG APP Monitor'")
                    except Exception as e:
                        # Логируем любую ошибку при запуске приложения
                        self.save_log_file(f"ОШИБКА запуска приложения: {str(e)}")
                else:
                    # Логируем, что файл не найден
                    self.save_log_file(f"ОШИБКА: Файл '{self._exe_path}' не найден!")

                time.sleep(5)  # Ждем 5 секунд перед следующей проверкой

            # Проверяем состояние программы
            if self.process and self.process.poll() is None:  # Если программа все еще работает
                # Запись о том, что программа работает
                self.save_log_file(f"'Windows CPG APP Monitor' работает")
            # Если программа завершена
            else:
                # Запись о том, что программа закрыта
                self.save_log_file("'Windows CPG APP Monitor' не запущено. Перезагрузка...\n")

            time.sleep(10)  # Ждем 10 секунд перед следующей проверкой состояния программы

    def save_log_file(self, message):
        """Метод для логирования ошибок в файл."""
        try:
            with open(self._log_file_path, "a", encoding="utf-8") as log_file:
                log_file.write(f"SERVICE_WIN({time.strftime('%Y-%m-%d %H:%M:%S')}) - {message}\n==================\n")
        except Exception as e:
            # Логируем ошибку при записи в лог-файл
            print(f"Ошибка при записи в лог: {str(e)}")  # Здесь можно заменить на другое логирование


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(SimpleService)  # Запуск службы
