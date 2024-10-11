# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

import gettext

import function

_ = gettext.gettext


###########################################################################
## Class LanguageWnd
###########################################################################

class LanguageWnd(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self,
                           parent,
                           id=wx.ID_ANY,
                           title=_(u"Выбор языка"),
                           pos=wx.DefaultPosition,
                           size=wx.Size(-1, -1),
                           style=wx.DEFAULT_DIALOG_STYLE
                           )

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Segoe UI"))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        sizer_main = wx.BoxSizer(wx.VERTICAL)

        sizer_btn = wx.BoxSizer(wx.HORIZONTAL)

        self.btn_ru = wx.Button(self, wx.ID_ANY, _(u"Русский"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_ru.SetLabelMarkup(_(u"Русский"))
        sizer_btn.Add(self.btn_ru, 0, wx.ALL, 10)

        self.btn_en = wx.Button(self, wx.ID_ANY, _(u"English"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_en.SetLabelMarkup(_(u"English"))
        sizer_btn.Add(self.btn_en, 0, wx.ALL, 10)

        self.btn_uk = wx.Button(self, wx.ID_ANY, _(u"Українська"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_uk.SetLabelMarkup(_(u"Українська"))
        sizer_btn.Add(self.btn_uk, 0, wx.ALL, 10)

        sizer_main.Add(sizer_btn, 0, wx.ALIGN_CENTER, 5)

        self.SetSizer(sizer_main)
        self.Layout()
        sizer_main.Fit(self)

        self.Centre(wx.BOTH)

        # Подключаемые события в программе ----------------
        self.btn_ru.Bind(wx.EVT_BUTTON, lambda event: self.update_language('ru'))
        self.btn_en.Bind(wx.EVT_BUTTON, lambda event: self.update_language('en'))
        self.btn_uk.Bind(wx.EVT_BUTTON, lambda event: self.update_language('uk'))
        # END ---------------------------------------------


    # Обработчики событий --------------------------------
    def update_language(self, lang_code):
        function.update_data_json("language", lang_code)  # Сохраняем выбранный язык
        self.Destroy()  # Закрываем текущее окно
        print("--окно языка закрыто--")
        # wx.CallAfter(self.Destroy)  # Закрываем текущее окно


def main():
    app = wx.App(False)
    time_app = LanguageWnd(None)
    time_app.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()
