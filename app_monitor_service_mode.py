# Приложение оповещения о работе службы мониторинга.
# Показывает статус работы службы (можно управлять работой службы).
import os
import wx
import time
import gettext
import subprocess
import threading
import config_app

_ = gettext.gettext

SERVICE_NAME = "WindowsCPGmonitorService"  # Укажите имя службы здесь


###########################################################################
## Class ServiceControlFrame
## Класс окна оповещения о работе службы мониторинга.
###########################################################################
class ServiceControlFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self,
                          parent,
                          id=wx.ID_ANY,
                          title=_("Статус работы службы"),
                          pos=wx.DefaultPosition,
                          size=wx.DefaultSize,
                          style=wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP
                          )

        self.SetSizeHints(wx.Size(600, 300), wx.Size(600, 300))
        # Установка шрифта
        self.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Segoe UI"))
        # Задаем фон окна
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INACTIVEBORDER))
        # Устанавливаем иконку для окна
        icon = wx.Icon(os.path.join(config_app.FOLDER_IMG, "monitor.ico"), wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        self.SetTitle(f"Service Control GUI ({SERVICE_NAME})")
        # self.SetSize((400, 250))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Поле для вывода состояния службы
        self.status_output = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        vbox.Add(self.status_output, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

        # Кнопка для запуска службы
        self.start_button = wx.Button(panel, label="Запустить службу")
        self.start_button.Bind(wx.EVT_BUTTON, self.on_start_service)
        vbox.Add(self.start_button, flag=wx.EXPAND | wx.ALL, border=5)

        # Кнопка для остановки службы
        self.stop_button = wx.Button(panel, label="Остановить службу")
        self.stop_button.Bind(wx.EVT_BUTTON, self.on_stop_service)
        vbox.Add(self.stop_button, flag=wx.EXPAND | wx.ALL, border=5)

        panel.SetSizer(vbox)
        self.Centre(wx.BOTH)

        # Создаем поток для мониторинга службы
        self.monitor_thread = threading.Thread(target=self.monitor_service_status)
        self.monitor_thread.daemon = True  # Чтобы поток завершился при выходе из программы
        self.monitor_thread.start()

        # Обновляем статус службы при запуске
        self.update_service_status()

    # Метод для запуска службы
    def on_start_service(self, event):
        self.status_output.SetValue("Запуск службы...")
        self.start_button.Disable()
        command = f'sc start {SERVICE_NAME}'
        threading.Thread(target=self.start_service_in_background, args=(command,)).start()

    # Метод для остановки службы
    def on_stop_service(self, event):
        self.status_output.SetValue("Остановка службы...")
        self.stop_button.Disable()
        command = f'sc stop {SERVICE_NAME}'
        threading.Thread(target=self.stop_service_in_background, args=(command,)).start()

    # Фоновый запуск службы с циклической проверкой статуса
    def start_service_in_background(self, command):
        run_command(command)
        time.sleep(10)  # Задержка, чтобы дать службе время запуститься
        self.wait_until_status("running")

    # Фоновая остановка службы с циклической проверкой статуса
    def stop_service_in_background(self, command):
        run_command(command)
        time.sleep(10)  # Задержка, чтобы дать службе время остановиться
        self.wait_until_status("stopped")

    # Ожидание изменения статуса службы
    def wait_until_status(self, expected_status):
        while True:
            status = check_service_status()
            if status == expected_status:
                wx.CallAfter(self.update_service_status)
                break
            time.sleep(2)  # Периодическая проверка каждые 2 секунды

    # Метод для обновления интерфейса в зависимости от статуса службы
    def update_service_status(self):
        status = check_service_status()
        if status == "running":
            print("ЗАПУЩЕНА")
            self.status_output.SetValue(f"Служба '{SERVICE_NAME}' - ЗАПУЩЕНА")
            self.start_button.Disable()
            self.stop_button.Enable()
        elif status == "stopped":
            print("ОСТАНОВЛЕНА")
            self.status_output.SetValue(f"Служба '{SERVICE_NAME}' - ОСТАНОВЛЕНА")
            self.start_button.Enable()
            self.stop_button.Disable()
        else:
            print("НЕИЗВЕСТНО")
            self.status_output.SetValue(f"Состояние службы '{SERVICE_NAME}' - НЕИЗВЕСТНОЕ состояние...")
            self.start_button.Disable()
            self.stop_button.Disable()

    # Фоновый мониторинг состояния службы
    def monitor_service_status(self):
        while True:
            wx.CallAfter(self.update_service_status)
            time.sleep(10)  # Обновляем статус каждые 10 секунд


# Функция для выполнения системной команды
def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return str(e)


# Функция для проверки состояния службы
def check_service_status():
    command = f'sc query {SERVICE_NAME}'
    result = run_command(command)

    if "RUNNING" in result:
        return "running"
    elif "STOPPED" in result:
        return "stopped"
    else:
        return "unknown"


# Запуск приложения
if __name__ == "__main__":
    app = wx.App(False)
    frame = ServiceControlFrame(None)
    frame.Show()
    app.MainLoop()
