import win32serviceutil  # Модуль для управления службами Windows
import win32service  # Модуль для работы с функционалом службы
import win32event  # Модуль для работы с системными событиями
import servicemanager  # Модуль для регистрации событий в журнале Windows
import subprocess  # Модуль для запуска новых процессов

class MyService(win32serviceutil.ServiceFramework):
    """
    Класс, представляющий службу Windows.
    """
    _svc_name_ = "AApTest"  # Имя службы
    _svc_display_name_ = "AApTest Application Monitor Service"  # Отображаемое имя службы
    _svc_description_ = "Service to run and monitor Notepad."  # Описание службы

    exe_path = r"C:\Windows\System32\notepad.exe"  # Путь к блокноту

    def __init__(self, args):
        """
        Конструктор службы. Инициализация базового класса и создание события остановки.
        """
        win32serviceutil.ServiceFramework.__init__(self, args)  # Инициализация родительского класса
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)  # Событие для остановки службы

    def SvcStop(self):
        """
        Метод, вызываемый при остановке службы.
        """
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)  # Сообщаем системе, что служба прекращает работу
        win32event.SetEvent(self.hWaitStop)  # Устанавливаем событие для остановки

    def SvcDoRun(self):
        """
        Метод, который запускается при старте службы.
        """
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED, (self._svc_name_, '')
                              )

        self.run()  # Запуск основного метода службы

    def run(self):
        """
        Запускает .exe файл и ожидает остановки.
        """
        try:
            # Запускаем блокнот
            subprocess.Popen(self.exe_path, creationflags=subprocess.CREATE_NEW_CONSOLE)  # Создаем новый консольный процесс
            servicemanager.LogInfoMsg(f"AApTest - Запуск {self.exe_path}")  # Логируем успешный запуск
        except Exception as e:
            # Записываем ошибку в системный журнал
            servicemanager.LogErrorMsg(f"Ошибка при запуске службы - AApTest: {str(e)}")

        # Ожидаем команду остановки
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

# Этот блок кода выполняется, если программа запущена напрямую
if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(MyService)
