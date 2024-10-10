#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

import wx
import os
import gettext
import function


class ErrorWindow(wx.Frame):
    def __init__(self, parent, title, lang_code='ru'):
        super(ErrorWindow, self).__init__(parent, title=title, size=(400, 200))

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

    def set_language(self, lang_code):
        """
        Устанавливает язык для локализации
        """
        # Путь к папке - locale
        locale_dir = os.path.join(os.getcwd(), 'locale')
        print("locale_dir ", locale_dir)

        # Загружаем переводы для указанного языка
        lang = gettext.translation('messages', localedir=locale_dir, languages=[lang_code])
        lang.install()  # Устанавливаем переводы
        global _  # Глобальная переменная для использования перевода
        _ = lang.gettext  # Присваиваем gettext метод для использования

    def update_language(self, lang_code):
        """
        Обновление языка и текста
        """
        self.set_language(lang_code)  # Устанавливаем новый язык
        self.text.SetLabel(_("Блокировка интерфейса").upper())  # Обновляем текст
        self.Layout()  # Перерисовываем окно
        function.update_data_json("language", lang_code)  # Сохраняем выбранный язык


def main():
    app = wx.App(False)
    # Получаем язык, если он существует, иначе по умолчанию 'ru'
    lang_code = function.read_data_json("language")
    # Создаем окно с выбранным языком
    frame = ErrorWindow(None, "Локализация ошибки", lang_code)
    app.MainLoop()  # Запускаем главный цикл приложения


if __name__ == '__main__':
    main()







