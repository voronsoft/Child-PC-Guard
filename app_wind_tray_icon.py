import os

import wx
import wx.adv

import config_app


###########################################################################
## TrayIcon
## Класс иконки в трее.
###########################################################################


class TrayIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        super(TrayIcon, self).__init__()
        self.frame = frame

        # Устанавливаем иконку для трея
        icon = wx.Icon(os.path.join(config_app.FOLDER_IMG, "icon.ico"), wx.BITMAP_TYPE_ICO)
        self.SetIcon(wx.Icon(icon), "Child PC Guard")

        # Подключаем события.
        # Добавляем контекстное меню для иконки в трее
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_click)  # При нажатии на левую кнопку мышки
        self.Bind(wx.adv.EVT_TASKBAR_RIGHT_DOWN, self.on_right_click)  # При нажатии на правую кнопку мышки

    def create_popup_menu(self):
        """Создание контекстного меню"""
        menu = wx.Menu()
        # restore_item = menu.Append(wx.ID_ANY, "Восстановить окно")
        exit_item = menu.Append(wx.ID_EXIT, "Выход")

        # self.Bind(wx.EVT_MENU, self.on_restore, restore_item)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)

        return menu

    def on_left_click(self, event):
        """Обрабатывает левый клик по иконке трея"""
        self.on_restore(event)

    def on_right_click(self, event):
        """Обрабатывает правый клик по иконке трея"""
        self.PopupMenu(self.create_popup_menu())

    def on_restore(self, event):
        """Восстановление/сворачивание окна приложения при клике на иконку в трее"""
        if self.frame.IsIconized() or not self.frame.IsShown():
            # Если окно свернуто или скрыто, показываем его
            self.frame.Iconize(False)  # Убираем иконку из панели задач
            self.frame.Show(True)  # Показываем окно
            self.frame.Raise()  # Поднимаем его поверх других
        else:
            # Если окно видно, сворачиваем его
            self.frame.Iconize(True)  # Сворачиваем в панель задач
            self.frame.Show(False)  # Скрываем окно

    def on_exit(self, event):
        """Закрытие приложения"""
        wx.CallAfter(self.frame.Close)
