import os
import wx
import wx.xrc
import gettext
import function
import config_localization
from config_app import FOLDER_IMG

# Подключаем локализацию
_ = config_localization.setup_locale(function.read_data_json("language"))


###########################################################################
## Class WndInputFirstAppPass
## Класс начального ввода пароля для приложения
###########################################################################

class WndInputFirstAppPass(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self,
                           parent,
                           id=wx.ID_ANY,
                           title=_("Настройка программы"),
                           pos=wx.DefaultPosition,
                           size=wx.Size(600, 600),
                           style=wx.DEFAULT_DIALOG_STYLE
                           )

        # self.SetSizeHints(wx.Size(-1, -1), wx.Size(-1, -1))
        self.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Segoe UI"))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))

        sizer_main = wx.BoxSizer(wx.VERTICAL)

        sizer_main.SetMinSize(wx.Size(-1, -1))
        sizer_top = wx.BoxSizer(wx.VERTICAL)

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
        sizer_top.Add(self.attention_txt, 0, wx.EXPAND | wx.ALL, 5)
        # sizer_main.Add(sizer_lang, 0, wx.EXPAND | wx.ALL, 5)


        self.m_bitmap1 = wx.StaticBitmap(self,
                                         wx.ID_ANY,
                                         wx.Bitmap(os.path.join(FOLDER_IMG, "settings48.ico"), wx.BITMAP_TYPE_ANY),
                                         wx.DefaultPosition,
                                         wx.DefaultSize,
                                         0
                                         )
        sizer_top.Add(self.m_bitmap1, 0, wx.EXPAND | wx.ALL, 0)

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

        self.m_staticline = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        sizer_top.Add(self.m_staticline, 0, wx.EXPAND | wx.ALL, 10)

        # --------------------------------------------------------------------------------------------------
        self.m_bitmap2 = wx.StaticBitmap(self,
                                         wx.ID_ANY,
                                         wx.Bitmap(os.path.join(FOLDER_IMG, "user48.ico"), wx.BITMAP_TYPE_ANY),
                                         wx.DefaultPosition,
                                         wx.DefaultSize,
                                         0
                                         )
        sizer_top.Add(self.m_bitmap2, 0, wx.ALIGN_CENTER | wx.ALL, 0)

        self.static_txt2 = wx.StaticText(self,
                                         wx.ID_ANY,
                                         _("Выберите пользователя которого НЕЛЬЗЯ БЛОКИРОВАТЬ"),
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
        sizer_top.Add(self.input_protect_user, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        sizer_main.Add(sizer_top, 0, wx.EXPAND, 5)

        # ------------------- lang ------------------
        sizer_lang = wx.BoxSizer(wx.VERTICAL)
        self.m_staticline1 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        sizer_lang.Add(self.m_staticline1, 0, wx.EXPAND | wx.ALL, 5)

        sizer_txt_lang = wx.BoxSizer(wx.HORIZONTAL)

        self.m_bitmap3 = wx.StaticBitmap(self,
                                         wx.ID_ANY,
                                         wx.Bitmap(os.path.join(FOLDER_IMG, "language48.ico"), wx.BITMAP_TYPE_ANY),
                                         wx.DefaultPosition,
                                         wx.DefaultSize,
                                         0
                                         )
        sizer_lang.Add(self.m_bitmap3, 0, wx.ALIGN_CENTER | wx.ALL, 0)

        self.stat_txt = wx.StaticText(self, wx.ID_ANY, _("Язык приложения: "), wx.DefaultPosition, wx.DefaultSize, 0)
        self.stat_txt.Wrap(-1)
        self.stat_txt.SetForegroundColour(wx.Colour(255, 0, 0))
        sizer_txt_lang.Add(self.stat_txt, 0, 0, 5)

        self.lang_choice = wx.StaticText(self, wx.ID_ANY, "RU", wx.DefaultPosition, wx.DefaultSize, 0)
        self.lang_choice.Wrap(-1)
        self.lang_choice.SetFont(wx.Font(14,
                                         wx.FONTFAMILY_SWISS,
                                         wx.FONTSTYLE_NORMAL,
                                         wx.FONTWEIGHT_BOLD,
                                         False,
                                         "Segoe UI Semibold"
                                         )
                                 )
        self.lang_choice.SetForegroundColour(wx.Colour(255, 0, 0))
        sizer_txt_lang.Add(self.lang_choice, 0, 0, 5)

        sizer_lang.Add(sizer_txt_lang, 0, wx.ALIGN_CENTER, 5)

        sizer_btn_lang = wx.BoxSizer(wx.HORIZONTAL)

        self.btn_uk = wx.Button(self, wx.ID_ANY, "Українська", wx.DefaultPosition, wx.DefaultSize, 0)
        sizer_btn_lang.Add(self.btn_uk, 0, wx.ALIGN_CENTER, 5)

        self.btn_en = wx.Button(self, wx.ID_ANY, "English", wx.DefaultPosition, wx.DefaultSize, 0)
        sizer_btn_lang.Add(self.btn_en, 0, wx.ALL, 5)

        self.btn_ru = wx.Button(self, wx.ID_ANY, "Русский", wx.DefaultPosition, wx.DefaultSize, 0)
        sizer_btn_lang.Add(self.btn_ru, 0, wx.ALL, 5)

        sizer_lang.Add(sizer_btn_lang, 0, wx.ALIGN_CENTER, 5)

        self.m_staticline2 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        sizer_lang.Add(self.m_staticline2, 0, wx.EXPAND | wx.ALL, 5)

        sizer_main.Add(sizer_lang, 0, wx.EXPAND | wx.ALL, 5)
        # ------------------- end lang ------------------

        btn_sizer = wx.StdDialogButtonSizer()
        self.btn_sizerOK = wx.Button(self, wx.ID_OK)
        btn_sizer.AddButton(self.btn_sizerOK)
        self.btn_sizerCancel = wx.Button(self, wx.ID_CANCEL)
        btn_sizer.AddButton(self.btn_sizerCancel)
        btn_sizer.Realize()
        sizer_main.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.SetSizer(sizer_main)
        self.Layout()

        self.Centre(wx.BOTH)

        # Подключаемые события в программе ---------------
        self.Bind(wx.EVT_CLOSE, self.on_close)  # Событие, закрытия окна
        self.btn_sizerOK.Bind(wx.EVT_BUTTON, self.on_ok)  # Событие, нажатия OK
        self.btn_sizerCancel.Bind(wx.EVT_BUTTON, self.on_close)  # Событие, нажатия Cancel

        self.btn_uk.Bind(wx.EVT_BUTTON, lambda event: self.selection_language('uk'))
        self.btn_en.Bind(wx.EVT_BUTTON, lambda event: self.selection_language('en'))
        self.btn_ru.Bind(wx.EVT_BUTTON, lambda event: self.selection_language('ru'))

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
        # Получаем пользователя которого не блокировать
        usr = self.input_protect_user.GetValue()  # Получаем имя пользователя
        # Считываем пароль из БД (реестра)
        password_from_registry = function.get_password_from_registry()
        # Если поле ввода не менее 5ти знаков и пароль БД не пустой.
        if len(psw) >= 5 and password_from_registry is False:
            if usr:
                # Хешируем пароль для записи в БД
                psw_code = function.hash_password(self.input_txt_pass.GetValue())

                # Записываем пароль в реестр
                function.set_password_in_registry(psw_code)
                # Записываем Пользователя в БД (пользователь, который будет под защитой от блокировки)
                function.update_data_json("protected_user", usr)

                dialog = wx.MessageDialog(self,
                                          f"{_("Пароль ЗАПИСАН в программу.\nПользователь ЗАПИСАН в программу\nЯзык программы - ")}{function.read_data_json("language")}",
                                          _("ОТЛИЧНО"),
                                          wx.ICON_AUTH_NEEDED
                                          )
                dialog.ShowModal()
                dialog.Destroy()
                self.Destroy()
            else:
                dialog = wx.MessageDialog(self,
                                          _("Вы не выбрали пользователя которого нельзя блокировать"),
                                          _("ОШИБКА"),
                                          wx.ICON_AUTH_NEEDED
                                          )
                dialog.ShowModal()
                dialog.Destroy()
        elif len(psw) >= 5 and password_from_registry:
            # Выводим сообщение об ошибке, что пароль уже есть в бД
            wx.MessageBox(_("Пароль уже есть в БД"), _("Ошибка"), wx.OK | wx.ICON_ERROR)
        elif len(psw) <= 5:
            dialog = wx.MessageDialog(self, _("Пароль не может быть меньше пять знаков"), _("Предупреждение"), wx.ICON_WARNING)
            dialog.ShowModal()
            dialog.Destroy()

    def selection_language(self, lang_code="ru"):
        """
            Выбор языка для приложения
        """
        # Записываем код языка в БД
        function.update_data_json("language", lang_code)
        # Показываем в окне выбор языка
        self.lang_choice.SetLabel(lang_code.upper())



def main():
    app = wx.App()
    frame = WndInputFirstAppPass(None)
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
