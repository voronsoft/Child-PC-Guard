"""
Модуль соглашения, что программа не является подозрительным приложением или вирусом.
"""
import ctypes
import subprocess
import sys

import wx
import wx.html2
import wx.xrc

import config_localization
import function
from config_app import FOLDER_INSTALL_APP
from lang_app_wnd_add_app_defender_text import (en_html_txt_agreement,
                                                ru_html_txt_agreement,
                                                uk_html_txt_agreement)

# Подключаем локализацию
_ = config_localization.setup_locale(function.read_data_json("language"))


###########################################################################
# Class AddAppWindDefender
# Класс окна соглашения о том что устанавливаемое приложение не является вирусом или подозрительным приложением.
###########################################################################

class AddAppWindDefender(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=_(r"Добавить в исключения"), pos=wx.DefaultPosition, size=wx.Size(700, 700), style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.Size(700, 700), wx.Size(700, 700))
        self.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Segoe UI"))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))
        self.path_folder_app = FOLDER_INSTALL_APP

        sizer_main = wx.BoxSizer(wx.VERTICAL)

        sizer_main.SetMinSize(wx.Size(700, 700))
        sizer_top = wx.BoxSizer(wx.VERTICAL)

        sizer_main.Add(sizer_top, 0, wx.EXPAND, 5)

        sizer_help = wx.BoxSizer(wx.VERTICAL)

        # ------------------------------------- HTML -----------------------------
        self.html_win = wx.html2.WebView.New(self,
                                             wx.ID_ANY,
                                             size=wx.Size(700, 700)
                                             )
        # Устанавливаем язык HTML-контент
        lang_doc = function.read_data_json("language")
        if lang_doc == "ru":
            self.html_win.SetPage(ru_html_txt_agreement, "")
        elif lang_doc == "en":
            self.html_win.SetPage(en_html_txt_agreement, "")
        elif lang_doc == "uk":
            self.html_win.SetPage(uk_html_txt_agreement, "")

        sizer_main.Add(self.html_win, 1, wx.ALL | wx.EXPAND, 5)
        # ------------------------------------- end HTML -------------------------

        sizer_main.Add(sizer_help, 1, wx.ALL | wx.EXPAND, 5)

        sizer_btn = wx.StdDialogButtonSizer()
        self.sizer_btnOK = wx.Button(self, wx.ID_OK)
        sizer_btn.AddButton(self.sizer_btnOK)
        self.sizer_btnCancel = wx.Button(self, wx.ID_CANCEL)
        sizer_btn.AddButton(self.sizer_btnCancel)
        sizer_btn.Realize()

        sizer_main.Add(sizer_btn, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(sizer_main)
        self.Layout()

        self.Centre(wx.BOTH)

        # Подключаемые события в программе ---------------
        self.sizer_btnOK.Bind(wx.EVT_BUTTON, self.on_add_to_defender)
        self.sizer_btnCancel.Bind(wx.EVT_BUTTON, self.on_close)

    # Обработчики событий
    def on_add_to_defender(self, event):
        """Обработчик добавления папки в исключения Windows Defender"""
        if not self.restart_as_admin():
            return

        ps_script = f"""
        Add-MpPreference -ExclusionPath "{self.path_folder_app}"
        """
        try:
            subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-Command", ps_script], check=True, shell=True)
            wx.MessageBox(f"Папка {self.path_folder_app} успешно добавлена в исключения Windows Defender.", "Успех", wx.OK | wx.ICON_INFORMATION)
        except subprocess.CalledProcessError as e:
            wx.MessageBox(f"Ошибка при добавлении в исключения: {str(e)}", "Ошибка", wx.OK | wx.ICON_ERROR)

        self.Close()

    def on_close(self, event):
        """Обработчик закрытия программы"""
        self.Destroy()

    def restart_as_admin(self):
            """Проверка и перезапуск программы с правами администратора"""
            if ctypes.windll.shell32.IsUserAnAdmin():
                return True
            else:
                wx.MessageBox("Для добавления папки в исключения нужны права администратора.", "Требуются права администратора", wx.OK | wx.ICON_WARNING)
                try:
                    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, None, None, 1)
                except Exception as e:
                    wx.MessageBox(f"Не удалось перезапустить программу с правами администратора: {str(e)}", "Ошибка", wx.OK | wx.ICON_ERROR)
                sys.exit()


def run_main_add_def():
    app = wx.App(False)
    wnd_add_def = AddAppWindDefender(None)
    wnd_add_def.ShowModal()
    app.MainLoop()


if __name__ == '__main__':
    run_main_add_def()
