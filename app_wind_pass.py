import os

import wx
import wx.xrc

import config_localization
from config_app import FOLDER_IMG
from function import (check_password, get_password_from_registry,
                      read_data_json, send_bot_telegram_message)

# Подключаем локализацию
_ = config_localization.setup_locale(read_data_json("language"))


###########################################################################
## Class WndPass
## Класс окна ввода пароля для программы
###########################################################################

class WndPass(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent,
                           id=wx.ID_ANY,
                           title=_("ВХОД"),
                           pos=wx.DefaultPosition,
                           size=wx.Size(400, 150),
                           # style=wx.DEFAULT_DIALOG_STYLE & ~(wx.CLOSE_BOX) | wx.STAY_ON_TOP
                           style=wx.DEFAULT_DIALOG_STYLE | wx.STAY_ON_TOP
                           )
        self.password_from_registry= get_password_from_registry()  # Пароль из БД
        self.password_check = False  # Флаг проверки правильности пароля

        # Установка минимального размера окна
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        # Установка шрифта
        self.SetFont(wx.Font(12,
                             wx.FONTFAMILY_SWISS,
                             wx.FONTSTYLE_NORMAL,
                             wx.FONTWEIGHT_SEMIBOLD,
                             False,
                             "Segoe UI"
                             )
                     )
        # Задаем фон окна
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INACTIVEBORDER))
        # Устанавливаем иконку для окна
        icon = wx.Icon(os.path.join(FOLDER_IMG, "password24.ico"), wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        # Основной вертикальный слайзер
        sizer_main = wx.BoxSizer(wx.VERTICAL)

        # Поле ввода пароля и кнопка OK
        sizer_input = wx.BoxSizer(wx.HORIZONTAL)
        self.m_static_text1 = wx.StaticText(self, wx.ID_ANY, _("Пароль: "), wx.DefaultPosition, wx.DefaultSize, 0)
        sizer_input.Add(self.m_static_text1, 0, wx.ALL, 5)

        # Поле для ввода текста
        self.m_text_ctrl1 = wx.TextCtrl(self,
                                        wx.ID_ANY,
                                        wx.EmptyString,
                                        wx.DefaultPosition,
                                        wx.Size(200, -1),
                                        wx.TE_PASSWORD | wx.BORDER_SIMPLE | wx.TE_PROCESS_ENTER
                                        )
        sizer_input.Add(self.m_text_ctrl1, 0, wx.ALL, 5)

        # Кнопка OK
        self.btn_ok = wx.Button(self, wx.ID_ANY, _("OK"), wx.DefaultPosition, wx.DefaultSize, 0)
        sizer_input.Add(self.btn_ok, 0, wx.ALL, 5)

        # Добавляем слайзер с вводом и кнопкой в главный слайзер
        sizer_main.Add(sizer_input, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        # Установка главного слайзера
        self.SetSizer(sizer_main)
        self.Layout()
        sizer_main.Fit(self)

        # Центровка окна
        self.Centre(wx.BOTH)

        # Кнопка ОК
        self.btn_ok.Bind(wx.EVT_BUTTON, self.on_ok)

        # Привязка событий
        self.m_text_ctrl1.Bind(wx.EVT_TEXT_ENTER, self.on_ok)  # Привязка нажатия Enter к полю для пароля
        self.btn_ok.SetDefault()  # Установка кнопки OK как кнопки по умолчанию для Enter
        self.Bind(wx.EVT_CLOSE, self.on_close)  # Событие, закрытия окна

    # Обработчики
    def on_ok(self, event):
        """Обработчик нажатия кнопки OK"""
        # Сравниваем пароли из БД и поля для ввода
        if check_password(self.m_text_ctrl1.GetValue(), self.password_from_registry):
            self.password_check = True
            self.Destroy()  # Закрытие окна и завершение процесса
        else:
            wx.MessageBox(_("Неверный пароль. Попробуйте снова."), _("Ошибка"), wx.OK | wx.ICON_ERROR)
            send_bot_telegram_message(_("Кто то пытается разблокировать интерфейс программы\nПароль не совпал"))

    def on_close(self, event):
        """Обработчик закрытия программы"""
        print("Попытка закрытия окна")
        # Закрытие приложения
        self.Destroy()



if __name__ == "__main__":
    app = wx.App(False)
    main_frame = WndPass(None)
    main_frame.ShowModal()  # Используем ShowModal для модального окна
    app.MainLoop()
