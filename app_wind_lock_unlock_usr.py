import os

import wx
import wx.xrc

import gettext

from config_app import FOLDER_IMG

_ = gettext.gettext


###########################################################################
## Class UnblockUser
## Класс блокировки и разблокировки пользователя
###########################################################################

class UnblockUser(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self,
                           parent,
                           id=wx.ID_ANY,
                           title=_("Разблокировать пользователя"),
                           pos=wx.DefaultPosition,
                           size=wx.Size(400, 200),
                           style=wx.DEFAULT_DIALOG_STYLE
                           )

        self.SetSizeHints(wx.Size(400, 200), wx.Size(400, 200))
        self.SetFont(wx.Font(12,
                             wx.FONTFAMILY_SWISS,
                             wx.FONTSTYLE_NORMAL,
                             wx.FONTWEIGHT_SEMIBOLD,
                             False,
                             "Segoe UI Semibold"
                             )
                     )
        # Задаем фон окна
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INACTIVEBORDER))
        # Устанавливаем иконку для окна
        icon = wx.Icon(os.path.join(FOLDER_IMG, "icon.ico"), wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        sizer_main = wx.BoxSizer(wx.VERTICAL)

        sizer_top = wx.BoxSizer(wx.VERTICAL)

        sizer_top.SetMinSize(wx.Size(400, 100))
        sizer_data_user = wx.BoxSizer(wx.HORIZONTAL)

        self.img_user = wx.StaticBitmap(self,
                                        wx.ID_ANY,
                                        wx.Bitmap(os.path.join(FOLDER_IMG, "user48.ico"), wx.BITMAP_TYPE_ANY),
                                        wx.DefaultPosition,
                                        wx.DefaultSize,
                                        0
                                        )
        sizer_data_user.Add(self.img_user, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.static_txt = wx.StaticText(self, wx.ID_ANY, _("Нет блокировки"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.static_txt.SetLabelMarkup(_("Нет блокировки"))
        self.static_txt.Wrap(-1)

        self.static_txt.SetFont(wx.Font(24,
                                        wx.FONTFAMILY_SWISS,
                                        wx.FONTSTYLE_NORMAL,
                                        wx.FONTWEIGHT_BOLD,
                                        False,
                                        "Segoe UI"
                                        )
                                )
        self.static_txt.SetForegroundColour(wx.Colour(223, 0, 0))

        sizer_data_user.Add(self.static_txt, 1, wx.ALL | wx.EXPAND, 10)

        sizer_top.Add(sizer_data_user, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        self.static_line = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        self.static_line.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        self.static_line.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        sizer_top.Add(self.static_line, 0, wx.EXPAND | wx.ALL, 5)

        sizer_btn = wx.BoxSizer(wx.HORIZONTAL)

        self.btn_update = wx.Button(self, wx.ID_ANY, _("Поиск"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_update.SetLabelMarkup(_("Поиск"))
        self.btn_update.SetBitmap(wx.Bitmap(os.path.join(FOLDER_IMG, "update.ico"), wx.BITMAP_TYPE_ANY))
        self.btn_update.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNTEXT))
        self.btn_update.SetBackgroundColour(wx.Colour(251, 249, 174))
        self.btn_update.Enable()
        sizer_btn.Add(self.btn_update, 1, wx.ALL | wx.EXPAND, 5)

        self.btn_unlock = wx.Button(self, wx.ID_ANY, _("UnLock"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_unlock.SetLabelMarkup(_("UnLock"))
        self.btn_unlock.SetBitmap(wx.Bitmap(os.path.join(FOLDER_IMG, "unlock.ico"), wx.BITMAP_TYPE_ANY))
        self.btn_unlock.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNTEXT))
        self.btn_unlock.SetBackgroundColour(wx.Colour(174, 255, 170))
        self.btn_unlock.Enable()
        sizer_btn.Add(self.btn_unlock, 1, wx.ALL | wx.EXPAND, 5)

        self.btn_lock = wx.Button(self, wx.ID_ANY, _("Lock"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_lock.SetLabelMarkup(_("Lock"))
        self.btn_lock.SetBitmap(wx.Bitmap(os.path.join(FOLDER_IMG, "lock.ico"), wx.BITMAP_TYPE_ANY))
        self.btn_lock.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNTEXT))
        self.btn_lock.SetBackgroundColour(wx.Colour(244, 200, 181))
        self.btn_lock.Enable()
        sizer_btn.Add(self.btn_lock, 1, wx.ALL | wx.EXPAND, 5)

        sizer_top.Add(sizer_btn, 0, wx.ALL | wx.EXPAND, 5)

        sizer_main.Add(sizer_top, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(sizer_main)
        self.Layout()

        self.Centre(wx.BOTH)


if __name__ == "__main__":
    print(os.path.join(FOLDER_IMG, "user48.ico"))
    app = wx.App(False)
    main_frame = UnblockUser(None)
    main_frame.ShowModal()
    app.MainLoop()
