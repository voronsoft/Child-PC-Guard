#!/usr/bin/env python
# -*- coding: utf-8 -*-
import wx
import os
import gettext


class ErrorWindow(wx.Frame):
    def __init__(self, parent, title, lang_code='ru'):
        super(ErrorWindow, self).__init__(parent, title=title, size=(300, 200))

        # Устанавливаем язык
        self.set_language(lang_code)

        # Панель и текст
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Текст выводится большими буквами
        self.text = wx.StaticText(panel, label=_("Блокировка интерфейса").upper(), style=wx.ALIGN_CENTER)
        font = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.text.SetFont(font)
        sizer.Add(self.text, 1, wx.EXPAND | wx.ALL, 20)

        # Кнопки переключения языков
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        ru_btn = wx.Button(panel, label="Русский")
        en_btn = wx.Button(panel, label="English")
        uk_btn = wx.Button(panel, label="Українська")

        btn_sizer.Add(ru_btn, 1, wx.EXPAND | wx.ALL, 5)
        btn_sizer.Add(en_btn, 1, wx.EXPAND | wx.ALL, 5)
        btn_sizer.Add(uk_btn, 1, wx.EXPAND | wx.ALL, 5)

        sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER)
        panel.SetSizer(sizer)

        # Обработчики событий для кнопок
        ru_btn.Bind(wx.EVT_BUTTON, lambda event: self.update_language('ru'))
        en_btn.Bind(wx.EVT_BUTTON, lambda event: self.update_language('en'))
        uk_btn.Bind(wx.EVT_BUTTON, lambda event: self.update_language('uk'))

        self.Centre()
        self.Show()

    def set_language(self, lang_code):
        """
        Устанавливает язык для локализации
        """
        # Путь к папке - locale
        locale_dir = os.path.join(os.getcwd(), 'locale')
        print("locale_dir ", locale_dir)

        lang = gettext.translation('messages', localedir=locale_dir, languages=[lang_code])
        lang.install()
        global _
        _ = lang.gettext

    def update_language(self, lang_code):
        """
        Обновление языка и текста
        """
        self.set_language(lang_code)
        self.text.SetLabel(_("Блокировка интерфейса").upper())
        self.Layout()


if __name__ == '__main__':
    app = wx.App(False)

    # Начальный язык — русский
    frame = ErrorWindow(None, "Локализация ошибки", "ru")
    app.MainLoop()
