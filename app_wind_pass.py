import wx
import wx.xrc

import gettext

_ = gettext.gettext


###########################################################################
## Class wnd_pass
## Класс окна ввода пароля для программы
###########################################################################

class WndPass(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=_("Ввод пароля"), pos=wx.DefaultPosition,
                           size=wx.Size(-1, -1), style=wx.DEFAULT_DIALOG_STYLE)
        # TODO ВАЖНО - изменить пароль для программы !!! (app_wind_pass.py)
        self.password = "123"
        self.password_check = False

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Segoe UI"))

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        sizer.SetMinSize(wx.Size(500, 70))
        self.m_static_text1 = wx.StaticText(self, wx.ID_ANY, _("Введите пароль: "), wx.DefaultPosition, wx.DefaultSize,
                                            0)
        self.m_static_text1.Wrap(-1)

        sizer.Add(self.m_static_text1, 0, wx.ALL, 5)

        self.m_text_ctrl1 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(200, -1),
                                        0 | wx.BORDER_SIMPLE)
        sizer.Add(self.m_text_ctrl1, 0, wx.ALL, 5)

        self.btn_ok = wx.Button(self, wx.ID_ANY, _("OK"), wx.DefaultPosition, wx.DefaultSize, 0)
        sizer.Add(self.btn_ok, 0, wx.ALL, 5)

        self.SetSizer(sizer)
        self.Layout()
        sizer.Fit(self)

        self.Centre(wx.BOTH)

        # Привязка событий
        self.btn_ok.Bind(wx.EVT_BUTTON, self.on_ok)  # Событие, при нажатии кнопки OK

    # Обработчики
    def on_ok(self, event):
        # Получаем значения из полей ввода
        if self.password == self.m_text_ctrl1.GetValue():
            self.password_check = True
            self.Close()
            self.Destroy()
        else:
            wx.MessageBox("Неверный пароль. Попробуйте снова.", "Ошибка", wx.OK | wx.ICON_ERROR)
