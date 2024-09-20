import wx
import wx.xrc
import gettext
import json
import os
import threading
import time
import ctypes
import sys

_ = gettext.gettext

# Имя мьютекса (должно быть уникальным для вашего приложения)
MUTEX_NAME = "Global\\Child_PC_Timer"


###########################################################################
## Class TimerApp
## Класс окна Таймера для пользователя
###########################################################################

class TimerApp(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self,
                          parent,
                          id=wx.ID_ANY,
                          title=_("Осталось времени"),
                          pos=wx.DefaultPosition,
                          size=wx.DefaultSize,
                          style=wx.DEFAULT_FRAME_STYLE
                          )

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        # Установка шрифта
        self.SetFont(wx.Font(20, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Segoe UI"))
        # Задаем фон окна
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INACTIVEBORDER))
        # Устанавливаем иконку для окна
        icon = wx.Icon('icon.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        # Таймер для обновления каждую секунду
        self.timer = wx.Timer(self)
        # Путь к файлу с временем
        self.json_file = r"data.json"

        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.SetMinSize(wx.Size(300, -1))
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.time_label = wx.StaticText(self,
                                        wx.ID_ANY,
                                        _("00:00:00"),
                                        wx.DefaultPosition,
                                        wx.Size(-1, -1),
                                        0
                                        )
        # Установка красного цвета тексту
        self.time_label.SetForegroundColour(wx.Colour(255, 0, 0))
        self.time_label.Wrap(-1)
        sizer.Add(self.time_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        sizer_main.Add(sizer, 1, wx.ALIGN_CENTER, 5)

        self.SetSizer(sizer_main)
        self.Layout()
        sizer_main.Fit(self)

        self.Centre(wx.BOTH)

        # Подключаемые события в программе
        self.Bind(wx.EVT_TIMER, self.update_time, self.timer)
        self.timer.Start(1000)  # обновление каждые 1000 миллисекунд (1 секунда)

        # Запуск потока для чтения времени
        self.update_thread = threading.Thread(target=self.update_time_loop)
        self.update_thread.daemon = True
        self.update_thread.start()

    # Обработчики
    def read_time_from_json(self):
        """Чтение времени из файла time.json"""
        if os.path.exists(self.json_file):
            with open(self.json_file, 'r') as f:
                data = json.load(f)
                return data.get("remaining_time", None)
        else:
            wx.CallAfter(wx.MessageBox, f"Файл {self.json_file} не найден", "Ошибка", wx.OK | wx.ICON_ERROR)
            # Логируем ошибку
            self.log_error(f"Child_PC_Timer({time.strftime('%Y-%m-%d %H:%M:%S')}) -"
                           f"Файл {self.json_file} не найден"
                           )
            wx.CallAfter(self.Close)  # Закрываем приложение при отсутствии файла
            return None

    def update_time(self, event):
        """Обновление времени каждую секунду"""
        remaining_time = self.read_time_from_json()
        if remaining_time is not None:
            if remaining_time > 0:
                self.time_label.SetLabel(self.seconds_to_hms(remaining_time))
            elif remaining_time == 0:
                self.time_label.SetLabel(f"00:00:00")
        else:
            self.time_label.SetLabel("ERROR")

    def update_time_loop(self):
        """Цикл обновления времени в фоновом потоке"""
        while True:
            wx.CallAfter(self.update_time, None)
            time.sleep(1)

    def seconds_to_hms(self, seconds):
        """
        Преобразует количество секунд в строку формата часы:минуты:секунды.

        :param seconds: Количество секунд (целое число).
        :return: Строка формата "часы:минуты:секунды".
        """
        # Вычисляем количество часов, минут и секунд
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60

        # Форматируем результат с ведущими нулями
        return f"{hours:02}:{minutes:02}:{secs:02}"

    def log_error(self, message):
        """Логирование ошибок в файл."""
        log_file_path = r"log_chpcgu.txt"
        try:
            with open(log_file_path, 'a', encoding="utf-8") as log_file:
                log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n==================\n")
        except Exception as e:
            print(f"(1)Ошибка при записи лога в файл лога: {str(e)}")
            ctypes.windll.user32.MessageBoxW(None, f"Ошибка при записи в файл лога:\n{str(e)}", "ОШИБКА", 0)


# =============================================================================================================

def main():
    # ------- Проверка кода ошибки -------
    # Создание мьютекса
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, MUTEX_NAME)
    error_code = ctypes.windll.kernel32.GetLastError()

    if error_code == 183:
        ctypes.windll.user32.MessageBoxW(None, f"Приложение << Child PC Timer >> уже запущено.", "ПРЕДУПРЕЖДЕНИЕ", 0)
        # Закрываем дескриптор мьютекса, так как он не нужен
        ctypes.windll.kernel32.CloseHandle(mutex)
        return
    elif error_code != 0:
        ctypes.windll.user32.MessageBoxW(None, f"Неизвестная ошибка:\n{error_code}", "ОШИБКА", 0)
        # Закрываем дескриптор мьютекса
        ctypes.windll.kernel32.CloseHandle(mutex)
        return
    # -------------- END ---------------

    app = wx.App(False)
    time_app = TimerApp(None)
    time_app.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()
