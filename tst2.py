# Рабочий скрипт службы.

import time
import win32event
import win32service
import servicemanager
import win32serviceutil


class SimpleService(win32serviceutil.ServiceFramework):
    _svc_name_ = "AppTestService"  # Имя службы
    _svc_display_name_ = "AppTestService"  # Отображаемое имя
    _svc_description_ = "A simple Python service for testing."  # Описание службы

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.running = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        self.running = False

    def SvcDoRun(self):
        try:
            servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                                  servicemanager.PYS_SERVICE_STARTED,
                                  (self._svc_name_, '')
                                  )
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)  # Сообщение о том, что служба запущена
            self.main()
        except Exception as e:
            servicemanager.LogErrorMsg(f"Error run Test service: {str(e)}")
            raise

    def main(self):
        log_file_path = r"C:\Users\voron\Documents\test_log.txt"  # Укажите путь к лог-файлу
        while self.running:
            with open(log_file_path, "a", encoding="utf-8") as log_file:
                log_file.write(f"Service is running at {time.ctime()}\n")
            time.sleep(10)  # Ждет 10 секунд перед следующей записью


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(SimpleService)
