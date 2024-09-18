import time
import subprocess
import os
import psutil


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
                    print(f"Приложение {self.app_path} уже запущено.")
                    return False

                # Если не запущено, запускаем
                self.process = subprocess.Popen(self.app_path)
                print(f"Приложение {self.app_path} успешно запущено.")
                return True
            else:
                self.log_error(f"Приложение не найдено по пути: {self.app_path}")
                return False
        except Exception as e:
            self.log_error(f"Ошибка при запуске приложения: {str(e)}")
            return False

    def stop_app(self):
        """Метод для остановки приложения."""
        if self.process:
            try:
                self.process.terminate()
                self.process.wait()
                self.process = None
                print(f"Приложение мониторинга было остановлено.")
            except Exception as e:
                self.log_error(f"Ошибка при остановке приложения: {str(e)}")

    def is_app_running(self):
        """Проверка, запущено ли приложение."""
        return self.process and self.process.poll() is None

    def log_error(self, message):
        """Метод для логирования ошибок в файл."""
        # log_file_path = r"C:\child_control\app_monitor_log.txt"
        log_file_path = r"app_monitor_log.txt"
        try:
            with open(log_file_path, 'a', encoding="utf-8") as log_file:
                log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n==================\n")
        except Exception as e:
            print(f"Ошибка при записи в файл лога: {str(e)}")

    def monitor(self):
        """Основной метод мониторинга приложения."""
        # Продолжаем работу даже если приложение уже запущено
        print("Запуск мониторинга приложения...")
        if not self.start_app():
            self.log_error("Не удалось запустить приложение.")

        try:
            while True:
                # Проверяем, работает ли приложение
                if not self.is_process_running(os.path.basename(self.app_path)):
                    self.log_error("Приложение было закрыто. Перезапуск...")
                    print("Приложение завершило работу. Перезапуск...")
                    self.start_app()
                time.sleep(10)  # Интервал проверки
        except KeyboardInterrupt:
            print("Мониторинг остановлен вручную.")
            self.stop_app()


if __name__ == '__main__':
    monitor = AppMonitor()
    monitor.monitor()
