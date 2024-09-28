import wx
import wx.xrc
import gettext
import json
import os
import threading
import time
import ctypes
import sys

import config_app
from function import read_json, function_to_create_path_data_files

_ = gettext.gettext

# Имя мьютекса (должно быть уникальным)
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
                          style=wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP
                          )

        self.SetSizeHints(wx.Size(300, 100), wx.Size(300, 100))
        # Установка шрифта
        self.SetFont(wx.Font(30, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Segoe UI"))
        # Задаем фон окна
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INACTIVEBORDER))
        # Устанавливаем иконку для окна
        icon = wx.Icon(os.path.join(config_app.FOLDER_IMG, "icon.ico"), wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        # Таймер для обновления каждую секунду
        self.timer = wx.Timer(self)
        # Путь к файлу с временем
        self.json_file = config_app.path_data_file

        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.SetMinSize(wx.Size(300, -1))
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.time_label = wx.StaticText(self,
                                        wx.ID_ANY,
                                        _("Выключен"),
                                        wx.DefaultPosition,
                                        wx.DefaultSize,
                                        0
                                        )
        # Установка красного цвета тексту
        self.time_label.SetForegroundColour(wx.Colour(255, 0, 0))
        self.time_label.Wrap(-1)
        sizer.Add(self.time_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 0)

        sizer_main.Add(sizer, 1, wx.ALIGN_CENTER, 5)

        self.SetSizer(sizer_main)
        self.Layout()
        sizer_main.Fit(self)

        self.Centre(wx.BOTH)

        # Подключаемые события в программе
        self.Bind(wx.EVT_TIMER, self.update_time, self.timer)  # если произошло событие таймера
        self.timer.Start(1000)  # обновление каждые 1000 миллисекунд (1 секунда)

        # Запуск потока для чтения времени
        self.update_thread = threading.Thread(target=self.update_time_loop)
        self.update_thread.daemon = True
        self.update_thread.start()

    def update_time(self, event):
        """Обработчик обновления времени каждую секунду"""
        remaining_time = read_json("remaining_time")
        print(remaining_time)
        if remaining_time is not None:
            if remaining_time > 0:
                self.time_label.SetLabel(self.seconds_to_hms(remaining_time))
                self.Layout()
            elif remaining_time == 0:
                self.time_label.SetLabel(f"Выключен")
        else:
            self.time_label.SetLabel("ERROR")
            self.timer.Stop()
            wx.CallAfter(wx.MessageBox,
                         f"Ошибка считывания времени.\nТаймер будет закрыт.\n"
                         f"Повторный запуск таймера может исправить проблему",
                         "Ошибка",
                         wx.OK | wx.ICON_ERROR
                         )
            # Проверка существования файлов с данными
            function_to_create_path_data_files()
            # Запускаем таймер
            self.timer.Start(1000)
            # self.Close(True)

    def update_time_loop(self):
        """Цикл обновления времени в фоновом потоке"""
        while True:
            if self.time_label.GetLabel() == "ERROR":
                print("Остановлен цикл", self.time_label.GetLabel())
                break
            else:
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
        try:
            with open(config_app.path_log_file, 'a', encoding="utf-8") as log_file:
                log_file.write(f"TIMER({time.strftime('%Y-%m-%d %H:%M:%S')}) - "
                               f"{message}\n==================\n"
                               )
        except Exception as e:
            print(f"(1)Ошибка при записи лога в файл: {str(e)}")
            ctypes.windll.user32.MessageBoxW(None, f"Ошибка при записи в файл лога:\n{str(e)}", "ОШИБКА", 0)


# =============================================================================================================

def main():
    # ------- Проверка кода ошибки -------
    # Создание мьютекса
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, MUTEX_NAME)
    error_code = ctypes.windll.kernel32.GetLastError()

    if error_code == 183 or error_code == 5:
        ctypes.windll.user32.MessageBoxW(None, f"Приложение Child PC Timer уже запущено.", "ПРЕДУПРЕЖДЕНИЕ", 0)
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
