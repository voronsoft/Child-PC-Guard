import os
import wx
import wx.xrc
import gettext
import function
from config_app import FOLDER_IMG

_ = gettext.gettext


###########################################################################
## Class WndInputFirstAppPass
## Класс начального ввода пароля для приложения
###########################################################################

class WndInputFirstAppPass(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self,
                           parent,
                           id=wx.ID_ANY,
                           title=_("Пароль программы"),
                           pos=wx.DefaultPosition,
                           size=wx.Size(600, 450),
                           style=wx.DEFAULT_DIALOG_STYLE
                           )

        # self.SetSizeHints(wx.Size(-1, -1), wx.Size(-1, -1))
        self.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Segoe UI"))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))

        sizer_main = wx.BoxSizer(wx.VERTICAL)

        sizer_main.SetMinSize(wx.Size(-1, -1))
        sizer_top = wx.BoxSizer(wx.VERTICAL)

        self.m_bitmap1 = wx.StaticBitmap(self,
                                         wx.ID_ANY,
                                         wx.Bitmap(os.path.join(FOLDER_IMG, "fingerprint.png"), wx.BITMAP_TYPE_ANY),
                                         wx.DefaultPosition,
                                         wx.DefaultSize,
                                         0
                                         )
        sizer_top.Add(self.m_bitmap1, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.attention_txt = wx.StaticText(self,
                                           wx.ID_ANY,
                                           _("Если фон главного окна КРАСНОГО цвета,\n"
                                             "значит программа запущена без прав АДМИНИСТРАТОРА.\n"
                                             "Необходимо перезапустить программу от имени АДМИНИСТРАТОРА"
                                             ),
                                           wx.DefaultPosition,
                                           wx.DefaultSize,
                                           wx.ALIGN_CENTER_HORIZONTAL
                                           )

        self.attention_txt.Wrap(-1)
        self.attention_txt.SetFont(wx.Font(10,
                                           wx.FONTFAMILY_SWISS,
                                           wx.FONTSTYLE_NORMAL,
                                           wx.FONTWEIGHT_SEMIBOLD,
                                           False,
                                           "Segoe UI Semibold"
                                           )
                                   )
        self.attention_txt.SetForegroundColour(wx.Colour(225, 0, 0))

        sizer_top.Add(self.attention_txt, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.static_txt = wx.StaticText(self,
                                        wx.ID_ANY,
                                        _("Введите пароль для приложения"),
                                        wx.DefaultPosition,
                                        wx.DefaultSize,
                                        0
                                        )
        self.static_txt.Wrap(-1)

        self.static_txt.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))

        sizer_top.Add(self.static_txt, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.input_txt_pass = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(200, -1), 0)
        self.input_txt_pass.SetFont(wx.Font(12,
                                            wx.FONTFAMILY_SWISS,
                                            wx.FONTSTYLE_NORMAL,
                                            wx.FONTWEIGHT_SEMIBOLD,
                                            False,
                                            "Segoe UI Semibold"
                                            )
                                    )
        self.input_txt_pass.SetForegroundColour(wx.Colour(220, 16, 16))
        self.input_txt_pass.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INACTIVEBORDER))

        sizer_top.Add(self.input_txt_pass, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        # --------------------------------------------------------------------------------------------------
        self.static_txt2 = wx.StaticText(self,
                                         wx.ID_ANY,
                                         _("\nВведите имя пользователя которого НЕЛЬЗЯ БЛОКИРОВАТЬ"),
                                         wx.DefaultPosition,
                                         wx.DefaultSize,
                                         0
                                         )
        self.static_txt2.Wrap(-1)

        self.static_txt2.SetForegroundColour(wx.Colour(225, 0, 0))

        sizer_top.Add(self.static_txt2, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        user_list = function.get_users()
        if not user_list:
            user_list = [_("----")]

        self.input_protect_user = wx.ComboBox(self,
                                              wx.ID_ANY,
                                              wx.EmptyString,
                                              wx.DefaultPosition,
                                              wx.Size( 200,-1 ),
                                              choices=user_list,
                                              style=wx.CB_DROPDOWN | wx.CB_READONLY,
                                              )
        self.input_protect_user.SetSelection(-1)
        # sizer_top.Add(self.input_username, 0, wx.ALL, 5)
        sizer_top.Add(self.input_protect_user, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        sizer_main.Add(sizer_top, 1, wx.ALIGN_CENTER, 5)

        btn_sizer = wx.StdDialogButtonSizer()
        self.btn_sizerOK = wx.Button(self, wx.ID_OK)
        btn_sizer.AddButton(self.btn_sizerOK)
        self.btn_sizerCancel = wx.Button(self, wx.ID_CANCEL)
        btn_sizer.AddButton(self.btn_sizerCancel)
        btn_sizer.Realize()

        sizer_main.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        self.SetSizer(sizer_main)
        self.Layout()

        self.Centre(wx.BOTH)

        # Подключаемые события в программе ---------------
        self.Bind(wx.EVT_CLOSE, self.on_close)  # Событие, закрытия окна
        self.btn_sizerOK.Bind(wx.EVT_BUTTON, self.on_ok)  # Событие, нажатия OK
        self.btn_sizerCancel.Bind(wx.EVT_BUTTON, self.on_close)  # Событие, нажатия Cancel

    # Обработчики событий
    def on_close(self, event):
        """Обработчик закрытия окна"""
        self.Hide()
        self.Close()
        wx.Exit()

    def on_ok(self, event):
        """Обработчик нажатия кнопки ОК"""
        # Получаем пароль из поля ввода
        psw = self.input_txt_pass.GetValue()
        # Считываем пароль из БД (реестра)
        password_from_registry = function.get_password_from_registry()
        # Если поле ввода не менее 5ти знаков и пароль БД не пустой.
        if len(psw) >= 5 and password_from_registry is False:
            # Хешируем пароль для записи в БД
            psw_code = function.hash_password(self.input_txt_pass.GetValue())
            # Записываем пароль в реестр
            function.set_password_in_registry(psw_code)
            # Записываем Пользователя в БД (пользователь, который будет под защитой от блокировки)
            usr = self.input_protect_user.GetValue()  # Получаем имя пользователя
            function.update_data_json("protected_user", usr)

            dialog = wx.MessageDialog(self,
                                      _(f"Пароль ЗАПИСАН в программу.\nПользователь ЗАПИСАН в программу"),
                                      _("ОТЛИЧНО"),
                                      wx.ICON_AUTH_NEEDED
                                      )
            dialog.ShowModal()
            dialog.Destroy()
            self.Destroy()
        elif len(psw) >= 5 and password_from_registry:
            # Выводим сообщение об ошибке, что пароль уже есть в бД
            wx.MessageBox(_("Пароль уже есть в БД"), _("Ошибка"), wx.OK | wx.ICON_ERROR)
        elif len(psw) <= 5:
            dialog = wx.MessageDialog(self, _("Пароль не может быть меньше пять знаков"), _("Предупреждение"), wx.ICON_WARNING)
            dialog.ShowModal()
            dialog.Destroy()


def main():
    app = wx.App()
    frame = WndInputFirstAppPass(None)
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
