# import wx
# import json
# import os
# import threading
# import time
#
# class TimeApp(wx.Frame):
#     def __init__(self, *args, **kw):
#         super(TimeApp, self).__init__(*args, **kw)
#
#         # Установка фиксированного размера окна
#         self.SetSize((400, 150))
#         self.SetMinSize((400, 150))
#         self.SetMaxSize((400, 150))
#
#         # Установка окна всегда поверх всех
#         self.SetWindowStyle(self.GetWindowStyle() | wx.STAY_ON_TOP)
#
#         # Панель и метка для отображения времени
#         panel = wx.Panel(self)
#         self.time_label = wx.StaticText(panel, label="Загрузка времени...", pos=(50, 50))
#
#         # Таймер для обновления каждую секунду
#         self.timer = wx.Timer(self)
#         self.Bind(wx.EVT_TIMER, self.update_time, self.timer)
#         self.timer.Start(1000)  # обновление каждые 1000 миллисекунд (1 секунда)
#
#         # Файл JSON с временем
#         self.json_file = r"C:\Users\Public\Documents\timer.json"  # Укажите корректный путь к файлу
#
#         # Запуск потока для чтения времени
#         self.update_thread = threading.Thread(target=self.update_time_loop)
#         self.update_thread.daemon = True
#         self.update_thread.start()
#
#     def read_time_from_json(self):
#         """Чтение времени из файла time.json"""
#         if os.path.exists(self.json_file):
#             with open(self.json_file, 'r') as f:
#                 data = json.load(f)
#                 return data.get("remaining_time", None)
#         else:
#             wx.CallAfter(wx.MessageBox, f"Файл {self.json_file} не найден", "Ошибка", wx.OK | wx.ICON_ERROR)
#             wx.CallAfter(self.Close)  # Закрываем приложение при отсутствии файла
#             return None
#
#     def update_time(self, event):
#         """Обновление времени каждую секунду"""
#         remaining_time = self.read_time_from_json()
#         if remaining_time is not None:
#             if remaining_time > 0:
#                 self.time_label.SetLabel(f"Осталось времени: {remaining_time} сек")
#             elif remaining_time == 0:
#                 self.Close()  # Закрываем приложение, если время истекло
#         else:
#             self.time_label.SetLabel("Ошибка загрузки времени")
#
#     def update_time_loop(self):
#         """Цикл обновления времени в фоновом потоке"""
#         while True:
#             wx.CallAfter(self.update_time, None)
#             time.sleep(1)
#
# # Инициализация приложения
# if __name__ == "__main__":
#     app = wx.App(False)
#     frame = TimeApp(None, title="Время до включения блокировки", style=wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP)
#     frame.Show()
#     app.MainLoop()


import wx
import wx.xrc
import gettext
import json
import os
import threading
import time

_ = gettext.gettext


###########################################################################
## Class TimeApp
###########################################################################

class TimeApp(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self,
                          parent,
                          id=wx.ID_ANY,
                          title=_(u"Время включения блокировки"),
                          pos=wx.DefaultPosition,
                          size=wx.Size(350, 100),
                          style=wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP | wx.TAB_TRAVERSAL
                          )

        self.SetSizeHints(wx.Size(350, 100), wx.Size(350, 100))
        self.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Segoe UI"))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INACTIVEBORDER))

        # Таймер для обновления каждую секунду
        self.timer = wx.Timer(self)
        # Файл JSON с временем
        self.json_file = r"C:\Users\Public\Documents\timer.json"

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.time_label = wx.StaticText(self,
                                        wx.ID_ANY,
                                        _(u"Загрузка времени..."),
                                        wx.Point(-1, -1),
                                        wx.Size(-1, -1),
                                        0,
                                        )
        self.time_label.Wrap(-1)

        sizer.Add(self.time_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)

        self.SetSizer(sizer)
        self.Layout()

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
            wx.CallAfter(self.Close)  # Закрываем приложение при отсутствии файла
            return None

    def update_time(self, event):
        """Обновление времени каждую секунду"""
        remaining_time = self.read_time_from_json()
        if remaining_time is not None:
            if remaining_time > 0:
                self.time_label.SetLabel(f"Осталось времени: {remaining_time} ")
            elif remaining_time == 0:
                # self.Close()  # Закрываем приложение, если время истекло
                self.time_label.SetLabel(f"Блокировка отключена.")
        else:
            self.time_label.SetLabel("Ошибка загрузки времени")

    def update_time_loop(self):
        """Цикл обновления времени в фоновом потоке"""
        while True:
            wx.CallAfter(self.update_time, None)
            time.sleep(1)


# =============================================================================================================


def main():
    app = wx.App(False)
    time_app = TimeApp(None)
    time_app.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()
