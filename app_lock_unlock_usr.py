"""
Модуль разблокировки пользователя
"""

import ctypes
import os
import time
import subprocess

import wx
import wx.xrc

import config_localization
import function
from config_app import FOLDER_IMG, PATH_LOG_FILE

# Подключаем локализацию
_ = config_localization.setup_locale(function.read_data_json("language"))

# Имя мьютекса (должно быть уникальным)
MUTEX_NAME_UUCPG = "Global\\Unlock_User_CPGuard"
# Определяем режим работы приложения
APP_MODE = bool(ctypes.windll.shell32.IsUserAnAdmin())


class Pass(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent,
                           id=wx.ID_ANY,
                           title=_("ВВЕДИТЕ ПАРОЛЬ"),
                           pos=wx.DefaultPosition,
                           size=wx.Size(400, 150),
                           style=wx.DEFAULT_DIALOG_STYLE | wx.STAY_ON_TOP
                           )
        self.SetSizeHints(wx.Size(400, 150), wx.Size(400, 150))
        self.password_from_registry = function.get_password_from_registry()  # Пароль из БД
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

        # Установка главного сайзера
        self.SetSizer(sizer_main)
        self.Layout()
        sizer_main.Fit(self)
        # Центровка окна
        self.Centre(wx.BOTH)

        # Привязка событий
        self.btn_ok.Bind(wx.EVT_BUTTON, self.on_ok)  # Кнопка ОК
        self.m_text_ctrl1.Bind(wx.EVT_TEXT_ENTER, self.on_ok)  # Привязка нажатия Enter к полю для пароля
        self.btn_ok.SetDefault()  # Установка кнопки OK как кнопки по умолчанию для Enter
        self.Bind(wx.EVT_CLOSE, self.on_close)  # Событие закрытие окна

    # Обработчик событий
    def on_ok(self, event):
        """Определяет поведение окна исходя из введенного пароля (принять или вывести сообщение если нет)"""
        # Получаем значение из поля ввода пароля и сравниваем со значением из БД
        if not function.get_password_from_registry():
            wx.MessageBox(
                    _("Не задан пароль для главного приложения.\nОткройте главное приложение и задайте пароль для главной программы.\nПотом вернитесь и введите пароль опять, что-бы получить доступ"),
                    _("Ошибка"), wx.OK | wx.ICON_STOP
            )
        elif function.check_password(self.m_text_ctrl1.GetValue(), self.password_from_registry):
            self.password_check = True
            self.Destroy()  # Закрытие окна и завершение процесса питон

        else:
            wx.MessageBox(_("Неверный пароль. Попробуйте снова."), _("Ошибка"), wx.OK | wx.ICON_ERROR)

    def on_close(self, event):
        """Закрывает родительское окно и текущее при закрытии"""
        self.GetParent().Destroy()  # Закрыть родительское окно
        self.Destroy()  # Закрыть текущее окно


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
        # Получаем имя заблокированного пользователя из системы
        self.USERNAME = function.get_block_user()

        sizer_main = wx.BoxSizer(wx.VERTICAL)

        sizer_top = wx.BoxSizer(wx.HORIZONTAL)

        sizer_static_text1 = wx.BoxSizer(wx.HORIZONTAL)

        self.static_txt_app_mode = wx.StaticText(self,
                                                 wx.ID_ANY,
                                                 ("Status program: " + _("АДМИНИСТРАТОР") if APP_MODE else _("НЕТ ПРАВ администратора")),
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

        sizer_static_text1.Add(self.static_txt_app_mode, 0, wx.ALIGN_CENTER, 10)

        sizer_top.Add(sizer_static_text1, 1, wx.ALIGN_CENTER | wx.ALL, 5)

        sizer_main.Add(sizer_top, 0, wx.ALL, 5)

        sizer_data_user = wx.BoxSizer(wx.HORIZONTAL)

        self.static_line0 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        sizer_main.Add(self.static_line0, 0, wx.ALL | wx.EXPAND, 5)

        self.img_user = wx.StaticBitmap(self,
                                        wx.ID_ANY,
                                        wx.Bitmap(os.path.join(FOLDER_IMG, "user48.ico"), wx.BITMAP_TYPE_ANY),
                                        wx.DefaultPosition,
                                        wx.Size(48, 48),
                                        0
                                        )
        sizer_data_user.Add(self.img_user, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.btn_update_mode = wx.BitmapButton(self,
                                                wx.ID_ANY,
                                                wx.NullBitmap,
                                                wx.DefaultPosition,
                                                wx.DefaultSize,
                                                wx.BU_AUTODRAW | 0
                                                )
        self.btn_update_mode.SetBitmap(wx.Bitmap(os.path.join(FOLDER_IMG, "update48.ico"), wx.BITMAP_TYPE_ANY))
        self.btn_update_mode.SetBitmapDisabled(wx.NullBitmap)
        self.btn_update_mode.SetBitmapPressed(wx.Bitmap(os.path.join(FOLDER_IMG, "update248.ico"), wx.BITMAP_TYPE_ANY))
        self.btn_update_mode.SetBitmapFocus(wx.NullBitmap)
        sizer_data_user.Add(self.btn_update_mode, 0, wx.ALIGN_CENTER | wx.ALL, 0)

        sizer_static_text2 = wx.BoxSizer(wx.HORIZONTAL)

        self.static_txt = wx.StaticText(self,
                                        wx.ID_ANY,
                                        f"{self.USERNAME if self.USERNAME else _('Нет заблокированных')}",
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
        sizer_static_text2.Add(self.static_txt, 1, wx.ALL | wx.EXPAND, 0)

        sizer_data_user.Add(sizer_static_text2, 1, wx.ALIGN_CENTER | wx.ALL, 5)
        # ---------------------------
        sizer_main.Add(sizer_data_user, 0, wx.ALL | wx.EXPAND, 0)

        self.static_line = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        sizer_main.Add(self.static_line, 0, wx.ALL | wx.EXPAND, 5)

        sizer_btn = wx.BoxSizer(wx.HORIZONTAL)

        self.btn_unlock = wx.Button(self, wx.ID_ANY, _("UnLock"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_unlock.SetBitmap(wx.Bitmap(os.path.join(FOLDER_IMG, "unlock32.ico"), wx.BITMAP_TYPE_ANY))
        self.btn_unlock.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNTEXT))
        self.btn_unlock.SetBackgroundColour(wx.Colour(174, 255, 170))
        # Состояние кнопки - "UnLock"
        if self.USERNAME == "":
            self.btn_unlock.Enable(False)
        elif not self.USERNAME:
            self.btn_unlock.Enable(False)
        else:
            self.btn_unlock.Enable(True)
        # ------- END "UnLock" --------
        sizer_btn.Add(self.btn_unlock, 1, wx.ALL | wx.EXPAND, 0)

        sizer_main.Add(sizer_btn, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(sizer_main)
        self.Layout()

        self.Centre(wx.BOTH)  # Центровка окна

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
        """Обработчик поиска заблокированного пользователя для 3 языковых версий"""
        self.USERNAME = function.get_block_user()

        if self.USERNAME:
            self.static_txt.SetLabel(self.USERNAME)
            self.btn_unlock.Enable(True)
        else:
            self.static_txt.SetLabel(_('Нет заблокированных'))

    def unblock(self, event):
        # Снимаем блокировку
        answer = self.unblock_user(self.USERNAME)
        # Очищаем имя пользователя для блокировки в файле
        function.update_data_json("username_blocking", "")
        # Очищаем время блокировки в файле
        function.update_data_json("remaining_time", 0)
        # Сбрасываем поле с именем пользователя
        self.static_txt.SetLabel(_("Нет заблокированных"))
        # Отключаем кнопку
        self.btn_unlock.Enable(False)
        if answer:
            # Сообщение записываем в log
            self.log_error(f"Пользователь {self.USERNAME} разблокирован !")
            function.show_message_with_auto_close(_("Пользователь {username} разблокирован.").format(username=self.USERNAME), _('Успешно'))
            function.send_bot_telegram_message(_("Пользователь {username} разблокирован.").format(username=self.USERNAME))

    def unblock_user(self, usr):
        """
        Разблокирует учетную запись пользователя Windows.

        :param usr: Имя учетной записи пользователя для разблокировки.
        """
        try:
            # Формируем команду для разблокировки пользователя
            command_enable_user = f'net user "{usr}" /active:yes'
            # Выполняем команду в командной строке
            subprocess.run(command_enable_user, shell=True, check=True)
            # subprocess.run(['runas', '/user:Administrator', f'cmd /c {command_enable_user}'], shell=True, check=True)

            return True
        except Exception as e:
            self.log_error(f"(unblock_user()) Ошибка при разблокировке пользователя - {usr}:\n{e}")
            function.show_message_with_auto_close(f"Ошибка при разблокировке пользователя - {usr}:\n{e}",
                                                  "Ошибка",
                                                  15
                                                  )
            return False

    @staticmethod
    def log_error(message):
        """Метод для логирования ошибок в файл."""
        try:
            with open(PATH_LOG_FILE, 'a', encoding='utf-8') as log_file:
                log_file.write(
                        f"CPG_UNLOCK_USER({time.strftime('%Y-%m-%d %H:%M:%S')}) -{message}\n==================\n"
                )
        except Exception as e:
            print(f"Ошибка при записи лога в файл лога: {str(e)}")
            function.show_message_with_auto_close(
                    f"CPG_UNLOCK_USER({time.strftime('%Y-%m-%d %H:%M:%S')}) - {message}\n==================\n",
                    _("Ошибка")
            )


def main():
    # Запускаем приложение как администратор
    function.run_as_admin()

    # ------- Проверка кода ошибки -------
    # Создание мьютекса
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, MUTEX_NAME_UUCPG)
    error_code = ctypes.windll.kernel32.GetLastError()

    function.process_mutex_error(error_code, mutex)
    # -------------- END ---------------

    app = wx.App(False)
    # Создаем главное окно
    main_frame = UnblockUser(None)

    # Создаем и отображаем окно ввода пароля
    pass_dialog = Pass(main_frame)  # Передаем ссылку на родительское окно
    pass_dialog.ShowModal()

    # Проверяем пароль если совпал отображаем главное окно
    if pass_dialog.password_check:
        main_frame.ShowModal()

    app.MainLoop()


if __name__ == "__main__":
    main()
