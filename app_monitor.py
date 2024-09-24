import ctypes
import time
import subprocess
import os
import psutil

from config_app import path_log_file

# Имя мьютекса (должно быть уникальным)
MUTEX_NAME = "Global\\Windows_CPG_Monitor"


class AppMonitor:
    def __init__(self):
        # Путь к приложению, которое будем запускать
        # self.app_path = r"C:\child_control\dist\Child PC Guard.exe"
        self.app_path = r"Child PC Guard.exe"
        self.process = None

    def is_process_running(self, process_name):
        """Проверяет, запущен ли процесс с данным именем."""
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] == process_name:
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return False

    def start_app(self):
        """Метод для запуска приложения."""
        try:
            if os.path.exists(self.app_path):
                # Проверяем, запущен ли процесс
                if self.is_process_running(os.path.basename(self.app_path)):
                    print(f"Приложение <<{self.app_path}>> уже запущено.")
                    self.log_error(f"Приложение <<{self.app_path}>> уже запущено.")
                    return False

                # Если не запущено, запускаем
                self.process = subprocess.Popen(self.app_path)
                print(f"Приложение <<{self.app_path}>> успешно запущено.")
                self.log_error(f"Приложение <<{self.app_path}>> успешно запущено.")
                return True
            else:
                print(f"Приложение <<{self.app_path}>> не найдено по пути: {self.app_path}")
                self.log_error(f"Приложение <<{self.app_path}>> не найдено по пути: {self.app_path}")
                return False
        except Exception as e:
            print(f"Ошибка при запуске приложения <<{self.app_path}>>:\n{str(e)}")
            self.log_error(f"Ошибка при запуске приложения <<{self.app_path}>>:\n{str(e)}")
            return False

    def stop_app(self):
        """Метод для остановки приложения."""
        if self.process:
            try:
                self.process.terminate()
                self.process.wait()
                self.process = None
                print(f"Приложение мониторинга было остановлено.")
                self.log_error(f"Приложение мониторинга было остановлено.")
            except Exception as e:
                print(f"Ошибка при остановке приложения:\n{str(e)}")
                self.log_error(f"Ошибка при остановке приложения:\n{str(e)}")

    def is_app_running(self):
        """Проверка, запущено ли приложение."""
        return self.process and self.process.poll() is None

    def log_error(self, message):
        """Метод для логирования ошибок в файл."""
        log_file_path = path_log_file
        try:
            with open(log_file_path, 'a', encoding="utf-8") as log_file:
                log_file.write(f"Windows_CPG_Monitor({time.strftime('%Y-%m-%d %H:%M:%S')}) -"
                               f" {message}\n==================\n"
                               )
        except Exception as e:
            print(f"Ошибка при записи лога в файл лога: {str(e)}")

    def monitor(self):
        """Основной метод мониторинга приложения."""
        # Продолжаем работу даже если приложение уже запущено
        print("Запуск мониторинга приложения...")
        if not self.start_app():
            self.log_error("Не удалось запустить приложение: <<Child PC Guard>>.")

        try:
            while True:
                # Проверяем, работает ли приложение
                if not self.is_process_running(os.path.basename(self.app_path)):
                    self.log_error("Приложение <<Child PC Guard>> закрыто. Перезапуск...")
                    print("Приложение << Child PC Guard >> закрыто. Перезапуск...")
                    self.start_app()
                time.sleep(10)  # Интервал проверки
        except KeyboardInterrupt:
            self.log_error("Мониторинг << Windows_CPG_Monitor >> остановлен вручную.")
            print("Мониторинг остановлен вручную.")
            self.stop_app()


def main():
    # ------- Проверка кода ошибки -------
    # Создание мьютекса
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, MUTEX_NAME)
    error_code = ctypes.windll.kernel32.GetLastError()

    if error_code == 183:
        ctypes.windll.user32.MessageBoxW(None, f"Приложение Windows CPG Monitor уже запущено.",
                                         "ПРЕДУПРЕЖДЕНИЕ", 0
                                         )
        # Закрываем дескриптор мьютекса, так как он не нужен
        ctypes.windll.kernel32.CloseHandle(mutex)
        return
    elif error_code != 0:
        ctypes.windll.user32.MessageBoxW(None, f"Неизвестная ошибка:\n{error_code}", "ОШИБКА", 0)
        # Закрываем дескриптор мьютекса
        ctypes.windll.kernel32.CloseHandle(mutex)
        return
    # -------------- END ---------------

    monitor = AppMonitor()
    monitor.monitor()


if __name__ == '__main__':
    main()
