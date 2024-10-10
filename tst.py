#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time

import wx
import app_locale_base as alb
import function


class ErrorWindow(wx.Frame):
    def __init__(self, parent):
        super(ErrorWindow, self).__init__(parent, size=(400, 200))
        self.SetTitle(_("ОШИБКА"))

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

        # Добавляем кнопки в горизонтальный бокс-сайзер
        btn_sizer.Add(ru_btn, 1, wx.EXPAND | wx.ALL, 5)
        btn_sizer.Add(en_btn, 1, wx.EXPAND | wx.ALL, 5)
        btn_sizer.Add(uk_btn, 1, wx.EXPAND | wx.ALL, 5)

        # Добавляем кнопки в основной сайзер
        sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER)
        panel.SetSizer(sizer)

        # Обработчики событий для кнопок
        ru_btn.Bind(wx.EVT_BUTTON, lambda event: self.update_language('ru'))
        en_btn.Bind(wx.EVT_BUTTON, lambda event: self.update_language('en'))
        uk_btn.Bind(wx.EVT_BUTTON, lambda event: self.update_language('uk'))

        self.Centre()  # Центрируем окно на экране
        self.Show()  # Показываем окно

    def update_language(self, lang_code):
        """
        Обновление языка и текста с перезагрузкой приложения
        """
        function.update_data_json("language", lang_code)  # Сохраняем выбранный язык
        wx.CallAfter(self.Destroy)  # Закрываем текущее окно
        wx.CallAfter(main)


def main():
    app = alb.BaseApp(redirect=False)
    frame = ErrorWindow(None)
    frame.Show()
    app.MainLoop()  # Запускаем главный цикл приложения


if __name__ == '__main__':
    main()
