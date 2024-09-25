import os
import wx
import wx.xrc
import time
import ctypes
import gettext

import function
from config_app import FOLDER_IMG, path_log_file
from function import read_json, is_admin, run_as_admin, unblock_user

_ = gettext.gettext

# Имя мьютекса (должно быть уникальным)
MUTEX_NAME = "Global\\Unlock_User_CPGuard"

USERNAME = read_json('username_blocking')

TIME = read_json('remaining_time')

APP_MODE = bool(ctypes.windll.shell32.IsUserAnAdmin())



class UnblockUser(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self,
                           parent,
                           id=wx.ID_ANY,
                           title=_("Разблокировать пользователя"),
                           pos=wx.DefaultPosition,
                           size=wx.Size(450, -1),
                           style=wx.DEFAULT_DIALOG_STYLE
                           )

        self.SetFont(wx.Font(12,
                             wx.FONTFAMILY_SWISS,
                             wx.FONTSTYLE_NORMAL,
                             wx.FONTWEIGHT_NORMAL,
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

        sizer_top = wx.BoxSizer(wx.HORIZONTAL)

        self.btn_update_mode = wx.BitmapButton(self,
                                               wx.ID_ANY,
                                               wx.NullBitmap,
                                               wx.DefaultPosition,
                                               wx.DefaultSize,
                                               wx.BU_AUTODRAW | 0
                                               )
        self.btn_update_mode.SetBitmap(wx.Bitmap(r"img\update48.ico", wx.BITMAP_TYPE_ANY))
        self.btn_update_mode.SetBitmapDisabled(wx.NullBitmap)
        self.btn_update_mode.SetBitmapPressed(wx.Bitmap(r"img\update248.ico", wx.BITMAP_TYPE_ANY))
        self.btn_update_mode.SetBitmapFocus(wx.NullBitmap)
        sizer_top.Add(self.btn_update_mode, 0, wx.ALIGN_CENTER | wx.ALL, 0)

        sizer_static_text1 = wx.BoxSizer(wx.HORIZONTAL)

        self.static_txt_app_mode = wx.StaticText(self,
                                                 wx.ID_ANY,
                                                 _("АДМИНИСТРАТОР" if APP_MODE else "НЕТ ПРАВ администратора"),
                                                 wx.Point(-1, -1),
                                                 wx.DefaultSize,
                                                 0
                                                 )
        self.static_txt_app_mode.Wrap(-1)

        self.static_txt_app_mode.SetFont(wx.Font(12,
                                                 wx.FONTFAMILY_SWISS,
                                                 wx.FONTSTYLE_ITALIC,
                                                 wx.FONTWEIGHT_BOLD,
                                                 False,
                                                 "Arial"
                                                 )
                                         )
        self.static_txt_app_mode.SetForegroundColour(wx.Colour(213, 0, 0))

        sizer_static_text1.Add(self.static_txt_app_mode, 1, wx.ALL | wx.EXPAND, 10)

        sizer_top.Add(sizer_static_text1, 1, wx.ALIGN_CENTER | wx.ALL, 5)

        sizer_main.Add(sizer_top, 0, wx.ALL | wx.EXPAND, 5)

        sizer_data_user = wx.BoxSizer(wx.HORIZONTAL)

        self.img_user = wx.StaticBitmap(self,
                                        wx.ID_ANY,
                                        wx.Bitmap(r"img\user48.ico", wx.BITMAP_TYPE_ANY),
                                        wx.DefaultPosition,
                                        wx.Size(48, 48),
                                        0
                                        )
        sizer_data_user.Add(self.img_user, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        sizer_static_text2 = wx.BoxSizer(wx.HORIZONTAL)

        self.static_txt = wx.StaticText(self,
                                        wx.ID_ANY,
                                        _(f"{USERNAME if USERNAME else 'Нет заблокированных'}"),
                                        wx.DefaultPosition,
                                        wx.DefaultSize,
                                        0
                                        )
        self.static_txt.Wrap(-1)

        self.static_txt.SetFont(wx.Font(20,
                                        wx.FONTFAMILY_SWISS,
                                        wx.FONTSTYLE_NORMAL,
                                        wx.FONTWEIGHT_BOLD,
                                        False,
                                        "Segoe UI"
                                        )
                                )
        self.static_txt.SetForegroundColour(wx.Colour(223, 0, 0))

        sizer_static_text2.Add(self.static_txt, 1, wx.ALL | wx.EXPAND, 10)

        sizer_data_user.Add(sizer_static_text2, 1, wx.ALIGN_CENTER | wx.ALL, 5)

        sizer_main.Add(sizer_data_user, 0, wx.ALL | wx.EXPAND, 5)

        self.static_line = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        self.static_line.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        self.static_line.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        sizer_main.Add(self.static_line, 0, wx.ALL | wx.EXPAND, 5)

        szer_btn = wx.BoxSizer(wx.HORIZONTAL)

        self.btn_unlock = wx.Button(self, wx.ID_ANY, _("UnLock"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_unlock.SetBitmap(wx.Bitmap(r"img\unlock32.ico", wx.BITMAP_TYPE_ANY))
        self.btn_unlock.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNTEXT))
        self.btn_unlock.SetBackgroundColour(wx.Colour(174, 255, 170))
        # Состояние кнопки - "UnLock"
        if USERNAME == "":
            self.btn_unlock.Enable(False)
        else:
            self.btn_unlock.Enable(True)

        szer_btn.Add(self.btn_unlock, 1, wx.ALL | wx.EXPAND, 0)

        # Резервная кнопка
        # self.btn_lock = wx.Button(self, wx.ID_ANY, _("Lock"), wx.DefaultPosition, wx.DefaultSize, 0)
        # self.btn_lock.SetBitmap(wx.Bitmap(r"img\lock32.ico", wx.BITMAP_TYPE_ANY))
        # self.btn_lock.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNTEXT))
        # self.btn_lock.SetBackgroundColour(wx.Colour(244, 200, 181))
        # # Состояние кнопки - "UnLock"
        # if USERNAME == "":
        #     self.btn_lock.Enable(False)
        # else:
        #     self.btn_lock.Enable(True)
        # szer_btn.Add(self.btn_lock, 1, wx.ALL | wx.EXPAND, 0)
        sizer_main.Add(szer_btn, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(sizer_main)
        self.Layout()

        self.Centre(wx.BOTH)

        # Привязка событий
        self.Bind(wx.EVT_CLOSE, self.on_close)  # Событие при закрытии окна
        self.btn_update_mode.Bind(wx.EVT_BUTTON, self.search_user_block)  # Событие при нажатии на кнопку обновить
        self.btn_unlock.Bind(wx.EVT_BUTTON, self.unblock)  # Событие, при нажатии кнопки UNLOCK (запуск задания)

    # Обработчики
    def on_close(self, event):
        """Обработчик события закрытия окна"""
        self.Destroy()  # Закрытие текущего окна
        wx.Exit()  # Завершение основного цикла приложения

    def search_user_block(self, event):
        """Обработчик поиска заблокированного пользователя"""
        usr = read_json('username_blocking')
        if len(usr) >= 3:
            # обновляем поле с именем
            self.static_txt.SetLabel(usr)
            # Активируем кнопку
            self.btn_unlock.Enable(True)

    def unblock(self, event):
        # Снимаем блокировку
        answer = unblock_user(USERNAME)
        # Очищаем имя пользователя для блокировки в файле
        function.update_json("username_blocking", "")
        # Очищаем время блокировки в файле
        function.update_json("remaining_time", 0)
        # Сбрасываем поле с именем пользователя
        self.static_txt.SetLabel(f"Нет заблокированных")
        # Отключаем кнопку
        self.btn_unlock.Enable(False)
        # Сообщение записываем в log
        self.log_error(f"Пользователь {USERNAME} разблокирован !")


        if answer:
            ctypes.windll.user32.MessageBoxW(
                    None,
                    f"Пользователь {USERNAME} разблокирован !",
                    "Успешно",
                    1
            )
        else:
            # Сообщение записываем в log
            self.log_error(f"Ошибка при разблокировке пользователя: {USERNAME}")
            ctypes.windll.user32.MessageBoxW(
                    None,
                    f"(a_l_u_u)\nОшибка при разблокировке пользователя: {USERNAME}\n",
                    "Ошибка",
                    1
            )

    def log_error(self, message):
        """Метод для логирования ошибок в файл."""
        try:
            with open(path_log_file, 'a', encoding='utf-8') as log_file:
                log_file.write(f"CPG_UNLOCK_USER({time.strftime('%Y-%m-%d %H:%M:%S')}) -"
                               f" {message}\n==================\n"
                               )
        except Exception as e:
            print(f"Ошибка при записи лога в файл лога: {str(e)}")
            ctypes.windll.user32.MessageBoxW(
                    None,
                    f"CPG_UNLOCK_USER({time.strftime('%Y-%m-%d %H:%M:%S')}) - {message}\n==================\n",
                    "Ошибка",
                    1
            )


def main():
    # ------- Проверка кода ошибки -------
    # Создание мьютекса
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, MUTEX_NAME)
    error_code = ctypes.windll.kernel32.GetLastError()

    if error_code == 183 or error_code == 5:
        ctypes.windll.user32.MessageBoxW(None, f"Приложение Unlock User CPGuard уже запущено.",
                                         "ПРЕДУПРЕЖДЕНИЕ", 0
                                         )
        # Закрываем дескриптор мьютекса, так как он не нужен
        ctypes.windll.kernel32.CloseHandle(mutex)
        return
    elif error_code != 0:
        ctypes.windll.user32.MessageBoxW(None, f"Неизвестная ошибка:\n{error_code}", "ОШИБКА", 0)
        # Закрываем дескриптор мьютекса
        ctypes.windll.kernel32.CloseHandle(mutex)
        return
    # -------------- END ---------------

    if APP_MODE:
        app = wx.App(False)
        main_frame = UnblockUser(None)
        main_frame.ShowModal()
        app.MainLoop()
    else:
        # Запускаем приложение как администратор
        run_as_admin()

        app = wx.App(False)
        main_frame = UnblockUser(None)
        main_frame.ShowModal()
        app.MainLoop()


if __name__ == "__main__":
    main()
