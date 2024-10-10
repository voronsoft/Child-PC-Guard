# -*- coding: utf-8 -*-
import os

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.richtext

import gettext

from config_app import FOLDER_IMG

_ = gettext.gettext


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

        sizer_main.SetMinSize(wx.Size(700, 500))
        self.rich_txt = wx.richtext.RichTextCtrl(self,
                                                 wx.ID_ANY,
                                                 _("ТЕКСТ ЗАПОЛНИТЕЛЬ - документация в разработке\n"),
                                                 wx.DefaultPosition,
                                                 wx.Size(700, 450),
                                                 0 | wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER | wx.WANTS_CHARS  | wx.TE_READONLY
                                                 )

        self.rich_txt.SetFont(wx.Font(12,
                                      wx.FONTFAMILY_SWISS,
                                      wx.FONTSTYLE_NORMAL,
                                      wx.FONTWEIGHT_NORMAL,
                                      False,
                                      "Segoe UI"
                                      )
                              )
        self.rich_txt.SetMinSize(wx.Size(700, 450))
        self.rich_txt.SetMaxSize(wx.Size(700, 450))

        sizer_main.Add(self.rich_txt, 1, wx.ALL | wx.EXPAND, 5)

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


# Основная секция для запуска программы
if __name__ == '__main__':
    app = wx.App(False)
    doc_app = DocWindow(None)
    doc_app.Show()
    app.MainLoop()
