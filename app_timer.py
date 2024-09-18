import wx
import wx.xrc
import gettext
import json
import os
import threading
import time

_ = gettext.gettext


###########################################################################
## Class TimerApp
###########################################################################

class TimerApp(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self,
                          parent,
                          id=wx.ID_ANY,
                          title=_("Время включения блокировки"),
                          pos=wx.DefaultPosition,
                          size=wx.Size(350, 110),
                          style=wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP | wx.TAB_TRAVERSAL
                          )

        self.SetSizeHints(wx.Size(350, 110), wx.Size(350, 110))
        self.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Segoe UI"))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INACTIVEBORDER))
        # Устанавливаем иконку для окна
        icon = wx.Icon('icon.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        # Таймер для обновления каждую секунду
        self.timer = wx.Timer(self)
        # Путь к файлу с временем
        self.json_file = r"data.json"


        sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.time_label = wx.StaticText(self,
                                        wx.ID_ANY,
                                        _("Загрузка времени..."),
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
    time_app = TimerApp(None)
    time_app.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()
