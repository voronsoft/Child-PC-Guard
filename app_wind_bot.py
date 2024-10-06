import os
import wx
import wx.xrc
import gettext

from config_app import FOLDER_IMG

_ = gettext.gettext


###########################################################################
## Class BotWindow
## Класс окно для настройки оповещения через Telegram
###########################################################################

class BotWindow(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self,
                           parent,
                           id=wx.ID_ANY,
                           title=_("Настройка оповещения через Telegram"),
                           pos=wx.DefaultPosition,
                           size=wx.DefaultSize,
                           style=wx.DEFAULT_DIALOG_STYLE
                           )

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Segoe UI"))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))
        # Устанавливаем иконку для окна
        icon = wx.Icon(os.path.join(FOLDER_IMG, "telegram.ico"), wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        sizer_main = wx.BoxSizer(wx.VERTICAL)

        sizer_main.SetMinSize(wx.Size(700, 500))
        sizer_top = wx.BoxSizer(wx.VERTICAL)

        self.staticText1 = wx.StaticText(self,
                                         wx.ID_ANY,
                                         _("В этом окне, вам нужно ввести ID вашего чата с ботом программы.\n\n"
                                           "1- Откройте Telegram и в строке поиска введите: Child Pc Guard Bot или @ChildPCGuard_bot\n\n"
                                           "2- Для начала беседы нужно ввести /start или нажать кнопку Старт если она есть на экране.\n\n"
                                           "3- После этого вы получите сообщение от бота:"
                                           ),
                                         wx.DefaultPosition,
                                         wx.DefaultSize,
                                         0
                                         )
        self.staticText1.SetLabelMarkup(_(
                "В этом окне, вам нужно ввести ID вашего чата с ботом программы.\n\n"
                "1- Откройте Telegram и в строке поиска введите: Child Pc Guard Bot или @ChildPCGuard_bot\n\n"
                "2- Для начала беседы нужно ввести /start или нажать кнопку Старт если она есть на экране.\n\n"
                "3- После этого вы получите сообщение от бота:"
        )
        )
        self.staticText1.Wrap(-1)

        self.staticText1.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))

        sizer_top.Add(self.staticText1, 0, wx.ALL, 10)

        self.staticText2 = wx.StaticText(self,
                                         wx.ID_ANY,
                                         _("Ваш chat_id: хххххххххх\nЭтот номер вам нужно ввести в программе - Child PC Guard\n"
                                           "Нажав на кнопку в меню - 'Подключить оповещения через - Telegram'\n"
                                           "Введите номер в поле для ввода и нажмите - ОК\n"
                                           "После этого программа сможет понять кому отправлять сообщения"
                                           ),
                                         wx.DefaultPosition,
                                         wx.DefaultSize,
                                         0 | wx.BORDER_THEME
                                         )
        self.staticText2.SetLabelMarkup(_(
                "Ваш chat_id: хххххххххх\nЭтот номер вам нужно ввести в программе - Child PC Guard\n"
                "Нажав на кнопку в меню - 'Подключить оповещения через - Telegram'\n"
                "Введите номер в поле для ввода и нажмите - ОК\nПосле этого программа сможет понять кому отправлять сообщения"
        )
        )
        self.staticText2.Wrap(-1)

        self.staticText2.SetFont(wx.Font(9,
                                         wx.FONTFAMILY_SWISS,
                                         wx.FONTSTYLE_NORMAL,
                                         wx.FONTWEIGHT_NORMAL,
                                         False,
                                         "Segoe UI"
                                         )
                                 )
        self.staticText2.SetForegroundColour(wx.Colour(213, 0, 0))

        sizer_top.Add(self.staticText2, 0, wx.ALL, 10)

        self.staticText3 = wx.StaticText(self,
                                         wx.ID_ANY,
                                         _("4- Введите номер в поле что ниже и нажмите ОК.\n\n"
                                           "5- После этого программа будет присылать вам оповещение.\n\n"
                                           "6- Что бы получить доступ к меню бота, введите пароль от этой программы."
                                           ),
                                         wx.DefaultPosition,
                                         wx.DefaultSize,
                                         0
                                         )
        self.staticText3.SetLabelMarkup(_(
                "4- Введите номер в поле что ниже и нажмите ОК.\n\n"
                "5- После этого программа будет присылать вам оповещение.\n\n"
                "6- Что бы получить доступ к меню бота, введите пароль от этой программы."
        )
        )
        self.staticText3.Wrap(-1)

        self.staticText3.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))

        sizer_top.Add(self.staticText3, 0, wx.ALL, 10)

        self.m_staticline1 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        sizer_top.Add(self.m_staticline1, 0, wx.EXPAND | wx.ALL, 10)

        sizer_bottom = wx.BoxSizer(wx.VERTICAL)

        self.staticText4 = wx.StaticText(self,
                                         wx.ID_ANY,
                                         _("Ваш chat_id: (номер который вам выдаст бот)"),
                                         wx.DefaultPosition,
                                         wx.DefaultSize,
                                         0
                                         )
        self.staticText4.Wrap(-1)

        sizer_bottom.Add(self.staticText4, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.input_id_chat_bot = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(300, -1), 0)
        self.input_id_chat_bot.SetFont(wx.Font(12,
                                               wx.FONTFAMILY_SWISS,
                                               wx.FONTSTYLE_NORMAL,
                                               wx.FONTWEIGHT_NORMAL,
                                               False,
                                               "Segoe UI"
                                               )
                                       )

        sizer_bottom.Add(self.input_id_chat_bot, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        sizer_top.Add(sizer_bottom, 1, wx.EXPAND, 5)

        sizer_main.Add(sizer_top, 1, wx.EXPAND, 10)

        sizer_btn = wx.StdDialogButtonSizer()
        self.sizer_btnOK = wx.Button(self, wx.ID_OK)
        sizer_btn.AddButton(self.sizer_btnOK)
        self.sizer_btnCancel = wx.Button(self, wx.ID_CANCEL)
        sizer_btn.AddButton(self.sizer_btnCancel)
        sizer_btn.Realize()

        sizer_main.Add(sizer_btn, 0, wx.ALL | wx.EXPAND, 10)

        self.SetSizer(sizer_main)
        self.Layout()
        sizer_main.Fit(self)

        self.Centre(wx.BOTH)


# Основная секция для запуска программы
if __name__ == '__main__':
    app = wx.App(False)
    doc_app = BotWindow(None)
    doc_app.Show()
    app.MainLoop()
