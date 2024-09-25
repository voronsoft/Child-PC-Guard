import ctypes
import os
import shutil
import sys

import wx
import wx.xrc
import gettext

from config_app import FOLDER_IMG

_ = gettext.gettext


###########################################################################
## Class UninstallerFrame
###########################################################################

class UninstallerFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self,
                          parent,
                          id=wx.ID_ANY,
                          title=_("UNINSTALL Child PC Guard Suite"),
                          pos=wx.DefaultPosition,
                          size=wx.Size(600, 350),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL
                          )

        self.SetSizeHints(wx.Size(600, 350), wx.Size(600, 350))
        self.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Segoe UI"))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INACTIVEBORDER))
        # Устанавливаем иконку для окна
        icon = wx.Icon(os.path.join(FOLDER_IMG, "uninstall.ico"), wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.SetMinSize(wx.Size(600, 350))
        self.static_text = wx.StaticText(self,
                                         wx.ID_ANY,
                                         _("УДАЛЕНИЕ программ Child PC Guard Suite"),
                                         wx.DefaultPosition,
                                         wx.DefaultSize,
                                         0
                                         )
        self.static_text.Wrap(-1)

        sizer_main.Add(self.static_text, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.log_text = wx.TextCtrl(self,
                                    wx.ID_ANY,
                                    wx.EmptyString,
                                    wx.DefaultPosition,
                                    wx.DefaultSize,
                                    style=wx.TE_MULTILINE | wx.TE_READONLY
                                    )
        # Устанавливаем шрифт для текстового поля
        self.log_text.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        sizer_main.Add(self.log_text, 1, wx.ALL | wx.EXPAND, 5)

        sizer_ok = wx.StdDialogButtonSizer()
        self.btn_ok = wx.Button(self, wx.ID_OK)
        sizer_ok.AddButton(self.btn_ok)
        self.btn_cancel = wx.Button(self, wx.ID_CANCEL)
        sizer_ok.AddButton(self.btn_cancel)
        sizer_ok.Realize()
        sizer_main.Add(sizer_ok, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        self.SetSizer(sizer_main)
        self.Layout()
        self.Centre(wx.BOTH)

        # Привязываем события
        self.btn_ok.Bind(wx.EVT_BUTTON, self.on_confirm_uninstall)  # Событие при нажатии ОК
        self.btn_cancel.Bind(wx.EVT_BUTTON, self.on_cancel)  # Событие при нажатии CANCEL

    # Обработчики
    def on_confirm_uninstall(self, event):
        """Сообщение подтверждения удаления"""
        confirm_dialog = wx.MessageDialog(None,
                                          "Вы действительно хотите удалить все программы и файлы?",
                                          "Подтверждение удаления",
                                          wx.YES_NO | wx.NO_DEFAULT | wx.ICON_WARNING
                                          )
        if confirm_dialog.ShowModal() == wx.ID_YES:
            # Если пользователь подтвердил удаление, начинаем процесс удаления
            self.on_uninstall()
        else:
            self.log_message("Удаление отменено пользователем.")

    def on_uninstall(self):
        """Функция удаления приложений и всех зависимостей"""
        # Папка установки программ
        install_dir = os.path.join(os.getenv('ProgramFiles(x86)'), 'Child PC Guard')
        # Папка с данными для приложений (логи и json)
        common_data_dir = os.path.join(os.getenv('ProgramData'), 'Child PC Guard Data')
        # Папка с ярлыками из меню "Пуск"
        start_menu_dir = os.path.join(os.getenv('ProgramData'),
                                      'Microsoft',
                                      'Windows',
                                      'Start Menu',
                                      'Programs',
                                      'Child PC Guard'
                                      )
        # Папка с ярлыками на рабочем столе
        desktop_dir = os.path.join(os.getenv('Public'), 'Desktop')
        # Папка автозагрузки
        startup_dir = os.path.join(os.getenv('AppData'),
                                   'Microsoft',
                                   'Windows',
                                   'Start Menu',
                                   'Programs',
                                   'Startup'
                                   )

        # 1 Удаление исполняемых файлов и других данных
        try:
            if os.path.exists(install_dir):
                self.log_message(f"Удаление папки установки: {install_dir}")
                # Удаление папки с приложениями
                shutil.rmtree(install_dir)
                self.log_message("Папка установки удалена успешно.")
            else:
                self.log_message(f"Папка установки не найдена: {install_dir}")

            if os.path.exists(common_data_dir):
                self.log_message(f"Удаление папки данных: {common_data_dir}")
                # Удаление папки с данными для приложений (логи и json)
                shutil.rmtree(common_data_dir)
                self.log_message("Папка данных удалена успешно.")
            else:
                self.log_message(f"Папка данных не найдена: {common_data_dir}")
        except Exception as e:
            self.log_message(f"Ошибка при удалении папок:\n{e}")

        # 2 Удаление ярлыков из меню "Пуск"
        try:
            if os.path.exists(start_menu_dir):
                self.log_message(f"Удаление ярлыков из меню Пуск: {start_menu_dir}")
                shutil.rmtree(start_menu_dir)
                self.log_message("Ярлыки из меню Пуск удалены успешно.")
            else:
                self.log_message(f"Ярлыки в меню Пуск не найдены: {start_menu_dir}")
        except Exception as e:
            self.log_message(f"Ошибка при удалении ярлыков из меню Пуск:\n{e}")

        # 3 Удаление ярлыков с рабочего стола
        try:
            for shortcut in ['Child PC Guard.lnk', 'Child PC Timer.lnk',]:
                shortcut_path = os.path.join(desktop_dir, shortcut)
                if os.path.exists(shortcut_path):
                    self.log_message(f"Удаление ярлыка с рабочего стола: {shortcut_path}")
                    os.remove(shortcut_path)
                    self.log_message(f"Ярлык удален успешно: {shortcut_path}")
                else:
                    self.log_message(f"Ярлык не найден: {shortcut_path}")
        except Exception as e:
            self.log_message(f"Ошибка удаления ярлыков с рабочего стола:\n{e}")

        # 4 Удаление ярлыка из автозагрузки
        try:
            monitor_shortcut = os.path.join(startup_dir, 'Child PC Monitor.lnk')
            if os.path.exists(monitor_shortcut):
                self.log_message(f"Удаление ярлыка из автозагрузки: {monitor_shortcut}")
                os.remove(monitor_shortcut)
                self.log_message(f"Ярлык из автозагрузки удален успешно: {monitor_shortcut}")
            else:
                self.log_message(f"Ярлык автозагрузки не найден: {monitor_shortcut}")
        except Exception as e:
            self.log_message(f"Ошибка при удалении ярлыков из автозагрузки:\n{e}")

        # Сообщение об успешном удалении
        wx.MessageBox("Все программы и файлы успешно удалены!", "Удаление завершено", wx.OK | wx.ICON_INFORMATION)

        # 5 Запуск самоуничтожения
        # self.self_destruct()  # TODO Закомментировано в момент разработки

    def on_cancel(self, event):
        """Обработчик закрытия программы при нажатии кнопки CANCEL"""
        self.log_message("Деинсталляция отменена пользователем.")
        self.Close()

    def self_destruct(self):
        # TODO раскомментировать при релизе
        try:
            # Получаем путь к текущему исполняемому файлу
            current_exe = os.path.realpath(__file__)

            # Запуск команды удаления после закрытия текущего процесса
            delete_command = f'cmd /c timeout /t 3 && del /f /q "{current_exe}"'
            os.system(delete_command)

            # Закрываем приложение
            self.Close()
            ...
        except Exception as e:
            self.log_message(f"Ошибка при удалении самого деинсталлятора: {e}")

    def log_message(self, message):
        """Отображает сообщение в лог поле (self.log_text) и в консоли"""
        self.log_text.AppendText(message + "\n\n")
        print(message)


# ============================================================================================
def is_admin():
    """
    Проверяет, запущен ли скрипт с правами администратора.

    :return: True, если запущен с правами администратора, иначе False.
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def run_as_admin():
    """
    Проверяет, запущено ли приложение с правами администратора.
    Если нет, перезапускает его с запросом прав администратора.
    """
    if not is_admin():
        # Если приложение запущено без прав администратора, перезапускаем его с запросом прав администратора
        try:
            ctypes.windll.shell32.ShellExecuteW(
                    None,
                    "runas",
                    sys.executable,
                    ' '.join([f'"{arg}"' for arg in sys.argv]),
                    None,
                    0  # 1-отобразить консоль \ 0-скрыть консоль
            )
            sys.exit()  # Завершаем текущий процесс, чтобы предотвратить двойной запуск
        except Exception as e:
            ctypes.windll.user32.MessageBoxW(
                    None,
                    f"Не удалось запустить программу с правами администратора:\n\n{e}",
                    "Ошибка",
                    1
            )

def main():
    # Запускаем приложение как администратор
    run_as_admin()

    app = wx.App(False)
    uninst = UninstallerFrame(None)
    uninst.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()
