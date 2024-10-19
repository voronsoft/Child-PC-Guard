# -*- coding: utf-8 -*-
###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################
import os
import wx
import wx.xrc
import wx.html2
import function
import wx.richtext
import config_localization
from config_app import FOLDER_IMG
from lang_doc_text import ru_html_content, uk_html_content, en_html_content

# Подключаем локализацию
_ = config_localization.setup_locale(function.read_data_json("language"))


###########################################################################
## Class DocWindow
## Класс окна для документации
###########################################################################

class DocWindow(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self,
                           parent,
                           id=wx.ID_ANY,
                           title=_("Документация"),
                           pos=wx.DefaultPosition,
                           size=wx.DefaultSize,
                           style=wx.DEFAULT_DIALOG_STYLE
                           )

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Segoe UI"))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))
        # Устанавливаем иконку для окна
        icon = wx.Icon(os.path.join(FOLDER_IMG, "logs.ico"), wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        sizer_main = wx.BoxSizer(wx.VERTICAL)

        sizer_main.SetMinSize(wx.Size(700, 700))
        # ------------------------------------- HTML -----------------------------
        # Заменяем richtext контрол на HtmlWindow
        self.html_win = wx.html2.WebView.New(self,
                                           wx.ID_ANY,
                                           size=wx.Size(700, 700)
                                           )
        # Устанавливаем язык HTML-контент
        lang_doc = function.read_data_json("language")
        if lang_doc == "ru":
            self.html_win.SetPage(ru_html_content, "")
        elif lang_doc == "en":
            self.html_win.SetPage(en_html_content, "")
        elif lang_doc == "uk":
            self.html_win.SetPage(uk_html_content, "")

        sizer_main.Add(self.html_win, 1, wx.ALL | wx.EXPAND, 5)
        # ------------------------------------- end HTML -------------------------

        self.SetSizer(sizer_main)
        self.Layout()
        sizer_main.Fit(self)

        self.Centre(wx.BOTH)

        # Подключаемые события в программе ---------------
        self.Bind(wx.EVT_CLOSE, self.on_close)  # Событие, закрытия окна

    # Обработчики событий
    def on_close(self, event):
        """Обработчик закрытия программы"""
        self.Destroy()


def run_wind_doc():
    app = wx.App(False)
    doc_app = DocWindow(None)
    doc_app.Show()
    app.MainLoop()


if __name__ == '__main__':
    run_wind_doc()
