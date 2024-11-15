# -*- coding: utf-8 -*-
import sys
import wx


###########################################################################
## Class ScreenDialog
###########################################################################

class ScreenDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"Load Application", pos=wx.DefaultPosition, size=wx.Size(500, 120), style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.Size(500, 120), wx.Size(500, 120))

        sizer_main = wx.BoxSizer(wx.VERTICAL)

        sizer_main.SetMinSize(wx.Size(500, 120))
        sizer_top = wx.BoxSizer(wx.VERTICAL)

        self.static_txt = wx.StaticText(self, wx.ID_ANY, u"Loading...", wx.DefaultPosition, wx.DefaultSize, 0)
        self.static_txt.Wrap(-1)
        self.static_txt.SetFont(wx.Font(20, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, False, "Segoe UI"))
        self.static_txt.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        sizer_top.Add(self.static_txt, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        sizer_main.Add(sizer_top, 0, wx.EXPAND, 5)

        sizer_btm = wx.BoxSizer(wx.VERTICAL)

        self.gauge = wx.Gauge(self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL)
        self.gauge.SetValue(0)
        sizer_btm.Add(self.gauge, 0, wx.ALL | wx.EXPAND, 5)

        sizer_main.Add(sizer_btm, 1, wx.EXPAND, 5)

        self.SetSizer(sizer_main)
        self.Layout()
        self.Centre(wx.BOTH)

        # Добавляем таймер для обновления прогресс-бара
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
        self.count = 0  # Начальное значение прогресса

    def on_timer(self, event):
        if self.count < 100:
            self.count += 1
            self.gauge.SetValue(self.count)
        else:
            self.timer.Stop()  # Останавливаем таймер, когда прогресс достиг 100
            sys.exit(0)  # 0 обозначает успешное завершение

    def start_gauge(self):
        self.timer.Start(100)  # Запускаем таймер, обновляющий значение каждые 100 миллисекунд


def main_screensaver():
    app = wx.App(False)
    main_frame = ScreenDialog(None)
    main_frame.Show()
    main_frame.start_gauge()  # Запуск прогресс-бара
    app.MainLoop()


if __name__ == '__main__':
    main_screensaver()
