import os
import wx
import sys
import time
import wx.xrc
import ctypes
import gettext
import function
import subprocess

from app_wind_documentation import DocWindow
from app_wind_exit_prog import WndCloseApp
from app_wind_splash_screen import main_splash
from app_wind_pass import WndPass
from app_wind_tray_icon import TrayIcon
from config_app import FOLDER_IMG, path_timer_exe, path_monitor_exe, path_unblock_usr_exe, path_log_file

_ = gettext.gettext

# Имя мьютекса (должно быть уникальным)
MUTEX_NAME = "Global\\Child_PC_Guard"


###########################################################################
## Class Window
## Класс окна основного приложения
###########################################################################
class Window(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self,
                          parent,
                          id=wx.ID_ANY,
                          title=_("Child PC Guard - АДМИНИСТРАТОР"),
                          pos=wx.DefaultPosition,
                          size=wx.DefaultSize,
                          style=wx.DEFAULT_FRAME_STYLE & ~wx.MAXIMIZE_BOX | wx.TAB_TRAVERSAL
                          )

        self.SetSizeHints(wx.Size(700, 450), wx.Size(700, 450))
        self.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BACKGROUND))
        # Установка шрифта
        self.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Segoe UI"))
        # Задаем фон окна
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INACTIVEBORDER))
        # Устанавливаем иконку для окна
        icon = wx.Icon(os.path.join(FOLDER_IMG, "icon.ico"), wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        # Основные переменные ==========================================
        self.timer = wx.Timer(self)  # Таймеp
        self.username_blocking = function.read_json("username_blocking")  # Имя пользователя для блокировки из файла
        self.remaining_time = function.read_json("remaining_time")  # Время задаваемой блокировки из файла
        self.elapsed_time = 0  #

        # Определяем режим работы приложения, если не АДМИНИСТРАТОР фон красный окно не активно
        self.mode_run_app = function.check_mode_run_app()
        if self.mode_run_app != "admin":
            self.SetBackgroundColour(wx.Colour(255, 160, 160))  # Красный фон
            self.SetTitle("Child PC Guard - ПОЛЬЗОВАТЕЛЬ")  # Заголовок

        # ============================ END =============================
        # Создаем иконку в системном трее
        self.tray_icon = TrayIcon(self)

        # Тулбар =======================================================
        # self.tool_bar = self.CreateToolBar(wx.TB_TEXT, wx.ID_ANY)
        self.tool_bar = self.CreateToolBar(wx.TB_HORIZONTAL, wx.ID_ANY)
        self.tool_bar.SetToolSeparation(5)
        self.tool_bar.SetFont(wx.Font(8,
                                      wx.FONTFAMILY_SWISS,
                                      wx.FONTSTYLE_NORMAL,
                                      wx.FONTWEIGHT_NORMAL,
                                      False,
                                      "Segoe UI"
                                      )
                              )
        self.tool_bar.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))

        self.tool_bar.AddStretchableSpace()  # Вставляем гибкое пространство
        self.btn_tool_log = self.tool_bar.AddTool(wx.ID_ANY,
                                                  _(r"Логи"),
                                                  wx.Bitmap(os.path.join(FOLDER_IMG, "logs.ico"), wx.BITMAP_TYPE_ANY),
                                                  wx.NullBitmap,
                                                  wx.ITEM_NORMAL,
                                                  _(r"Логи"),
                                                  _(r"Просмотр логов программы"),
                                                  None
                                                  )
        # self.btn_tool_log.Enable(False)  # Отключение кнопки в тулбаре
        self.tool_bar.AddStretchableSpace()  # Вставляем гибкое пространство
        self.btn_tool_timer = self.tool_bar.AddTool(wx.ID_ANY,
                                                    _(r"Таймер"),
                                                    wx.Bitmap(os.path.join(FOLDER_IMG, "time.ico"), wx.BITMAP_TYPE_ANY),
                                                    wx.NullBitmap,
                                                    wx.ITEM_NORMAL,
                                                    _(r"Таймер "),
                                                    _(r"Открыть окно таймера"),
                                                    None
                                                    )
        # self.btn_tool2.Enable(False)  # Отключение кнопки в тулбаре
        self.tool_bar.AddStretchableSpace()  # Вставляем гибкое пространство
        self.btn_tool_monitor = self.tool_bar.AddTool(wx.ID_ANY,
                                                      _(r"Мониторинг"),
                                                      wx.Bitmap(os.path.join(FOLDER_IMG, "monitor.ico"),
                                                                wx.BITMAP_TYPE_ANY
                                                                ),
                                                      wx.NullBitmap,
                                                      wx.ITEM_NORMAL,
                                                      _(r"Мониторинг"),
                                                      _(r"Включить-отключить мониторинг"),
                                                      None
                                                      )
        self.tool_bar.AddStretchableSpace()  # Вставляем гибкое пространство
        self.btn_tool_clear_data = self.tool_bar.AddTool(wx.ID_ANY,
                                                         _(r"Очистить"),
                                                         wx.Bitmap(os.path.join(FOLDER_IMG, "clear.ico"),
                                                                   wx.BITMAP_TYPE_ANY
                                                                   ),
                                                         wx.NullBitmap,
                                                         wx.ITEM_NORMAL,
                                                         _(r"Очистить все"),
                                                         _(r"Удаляет все данные задания для блокировки. БЛОКИРОВКУ НЕ ОТКЛЮЧАЕТ"),
                                                         None
                                                         )
        self.tool_bar.AddStretchableSpace()  # Вставляем гибкое пространство
        self.btn_tool_run_unblock_usr = self.tool_bar.AddTool(wx.ID_ANY,
                                                              _(r"Разблокировать"),
                                                              wx.Bitmap(os.path.join(FOLDER_IMG, "unlock.ico"),
                                                                        wx.BITMAP_TYPE_ANY
                                                                        ),
                                                              wx.NullBitmap,
                                                              wx.ITEM_NORMAL,
                                                              _(r"Разблокировать пользователя"),
                                                              _(r"Открывает окно разблокировки пользователя"),
                                                              None
                                                              )
        self.tool_bar.AddStretchableSpace()  # Вставляем гибкое пространство
        self.btn_tool_info = self.tool_bar.AddTool(wx.ID_ANY,
                                                   _(r"Справка"),
                                                   wx.Bitmap(os.path.join(FOLDER_IMG, "doc.ico"), wx.BITMAP_TYPE_ANY),
                                                   wx.NullBitmap,
                                                   wx.ITEM_NORMAL,
                                                   _(r"Справка"),
                                                   _(r"Открывает окно по использованию программы"),
                                                   None
                                                   )
        self.tool_bar.AddStretchableSpace()  # Вставляем гибкое пространство

        self.btn_tool_unblock_interface = self.tool_bar.AddTool(wx.ID_ANY,
                                                                _(r"Разблокировать интерфейс"),
                                                                wx.Bitmap(os.path.join(FOLDER_IMG, "open.ico")),
                                                                wx.NullBitmap,
                                                                wx.ITEM_RADIO,
                                                                _(r"Разблокировать интерфейс"),
                                                                _(r"Разблокировать интерфейс"),
                                                                None
                                                                )
        self.btn_tool_block_interface = self.tool_bar.AddTool(wx.ID_ANY,
                                                              _(r"Заблокировать интерфейс"),
                                                              wx.Bitmap(os.path.join(FOLDER_IMG, "close.ico")),
                                                              wx.NullBitmap,
                                                              wx.ITEM_RADIO,
                                                              _(r"Заблокировать интерфейс"),
                                                              _(r"Блокировка интерфейса"),
                                                              None
                                                              )

        self.tool_bar.AddStretchableSpace()
        self.tool_bar.Realize()
        # ============================ END Туллбар =======================
        # Исходя из режима с какими правами запущена программа меняется фон окна приложения.

        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.SetMinSize(wx.Size(-1, -1))

        sizer_top = wx.BoxSizer(wx.HORIZONTAL)

        self.txt_input_username = wx.StaticText(self,
                                                wx.ID_ANY,
                                                _("Укажите пользователя для блокировки: "),
                                                wx.DefaultPosition,
                                                wx.DefaultSize,
                                                0
                                                )
        self.txt_input_username.Wrap(-1)
        sizer_top.Add(self.txt_input_username, 0, wx.ALL, 5)

        # Получаем список пользователей и создаем ComboBox
        user_list = function.get_users()

        if not user_list:
            user_list = [_("----")]
        self.input_username = wx.ComboBox(self, wx.ID_ANY, choices=user_list, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        # self.input_username.SetSelection(-1)
        sizer_top.Add(self.input_username, 0, wx.ALL, 5)
        sizer_main.Add(sizer_top, 0, wx.EXPAND, 5)

        self.staticline = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        sizer_main.Add(self.staticline, 0, wx.EXPAND | wx.ALL, 5)

        bSizer6 = wx.BoxSizer(wx.VERTICAL)

        sizer_main.Add(bSizer6, 1, wx.EXPAND, 5)

        sizer_top = wx.BoxSizer(wx.HORIZONTAL)

        self.txt_timer = wx.StaticText(self,
                                       wx.ID_ANY,
                                       _("Укажите время для блокировки:              "),
                                       wx.DefaultPosition,
                                       wx.DefaultSize,
                                       0
                                       )
        self.txt_timer.Wrap(-1)
        sizer_top.Add(self.txt_timer, 0, wx.ALL, 5)

        combo_box_choices = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

        self.input_time = wx.ComboBox(self,
                                      wx.ID_ANY,
                                      _("0"),
                                      wx.DefaultPosition,
                                      wx.DefaultSize,
                                      combo_box_choices,
                                      wx.CB_READONLY
                                      )
        # Устанавливаем начальное значение временем на 0
        self.input_time.SetSelection(0)

        self.input_time.SetMinSize(wx.Size(130, -1))

        sizer_top.Add(self.input_time, 0, wx.ALL, 5)

        self.txt_2 = wx.StaticText(self, wx.ID_ANY, _("час (0 отключено)"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.txt_2.Wrap(-1)

        sizer_top.Add(self.txt_2, 0, wx.ALL, 5)

        sizer_main.Add(sizer_top, 0, wx.EXPAND, 5)

        self.staticline = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        sizer_main.Add(self.staticline, 0, wx.EXPAND | wx.ALL, 5)

        sizer_center1 = wx.BoxSizer(wx.VERTICAL)
        self.txt_3 = wx.StaticText(self,
                                   wx.ID_ANY,
                                   _("Осталось времени до блокировки:"),
                                   wx.DefaultPosition,
                                   wx.DefaultSize,
                                   0
                                   )
        self.txt_3.Wrap(-1)

        sizer_center1.Add(self.txt_3, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.timer_time = wx.StaticText(self,
                                        wx.ID_ANY,
                                        _("00:00:00"),
                                        wx.DefaultPosition,
                                        wx.DefaultSize,
                                        0
                                        )
        self.timer_time.Wrap(-1)
        sizer_center1.Add(self.timer_time, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.gauge = wx.Gauge(self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL)
        sizer_center1.Add(self.gauge, 0, wx.ALL | wx.EXPAND, 5)
        sizer_main.Add(sizer_center1, 1, wx.ALL | wx.EXPAND, 5)

        sizer_center2 = wx.BoxSizer(wx.VERTICAL)
        self.btn_disable_blocking = wx.Button(self,
                                              wx.ID_ANY,
                                              _("Отключить блокировку"),
                                              wx.DefaultPosition,
                                              wx.DefaultSize,
                                              0
                                              )
        sizer_center2.Add(self.btn_disable_blocking, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.btn_disable_blocking.Disable()
        sizer_main.Add(sizer_center2, 1, wx.EXPAND, 5)

        sizer_bottom = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_ok = wx.Button(self, wx.ID_ANY, _("OK"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_ok.Disable()  # Деактивируем кнопку
        sizer_bottom.Add(self.btn_ok, 0, wx.ALL, 5)

        sizer_main.Add(sizer_bottom, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.status_bar = self.CreateStatusBar(1, wx.STB_SIZEGRIP, wx.ID_ANY)

        self.SetSizer(sizer_main)
        self.Layout()
        sizer_main.Fit(self)

        self.Centre(wx.BOTH)

        # ------------------------------------------------
        # TODO логика если есть остаточное время в файле.
        # Загрузка оставшегося времени из файла, если оно есть
        # Если есть остаточное время и имя в файле данных data.json
        if self.remaining_time > 0 and len(self.username_blocking) >= 1:
            # Отключаем кнопку OK
            # self.btn_ok.Enable(False)
            # Включаем кнопку - Отключить блокировку
            # self.btn_disable_blocking.Enable(True)
            # Определяем какой пользователь был выбран при продолжении отсчета времени если был остаток в файле.
            # Передав это значение в поле для отображения визуального понимания для какого пользователя считается
            # остаточное время
            self.input_username.SetValue(self.username_blocking)

            # Запускаем таймер, если есть оставшееся время
            self.elapsed_time = 0
            self.gauge.SetRange(self.remaining_time)
            self.gauge.SetValue(self.elapsed_time)
            self.timer.Start(1000)  # Запускаем таймер, обновляя каждую секунду
        # Если время 0 а имя пользователя есть
        elif self.remaining_time == 0 and len(self.username_blocking) >= 1:
            self.remaining_time = 0
        # Если время есть, а имени нет
        elif self.remaining_time > 0 and len(self.username_blocking) == 0:
            # Очищаем имя пользователя для блокировки в файле
            function.update_json("username_blocking", "")
            # Очищаем время блокировки в файле
            function.update_json("remaining_time", 0)
        # END - логика если есть остаточное время в файле.
        # ------------------------------------------------

        # Подключаемые события в программе ---------------
        self.input_username.Bind(wx.EVT_TEXT, self.on_input_changed)  # Событие при выборе имени пользователя
        self.input_time.Bind(wx.EVT_COMBOBOX, self.on_input_changed)  # Событие при выборе времени для блокировки

        self.Bind(wx.EVT_TIMER, self.run_on_timer, self.timer)  # Событие, при запуске таймера
        self.Bind(wx.EVT_CLOSE, self.on_close)  # Событие, закрытия окна
        self.btn_ok.Bind(wx.EVT_BUTTON, self.start_blocking)  # Событие, при нажатии OK (запуск задания)
        self.btn_disable_blocking.Bind(wx.EVT_BUTTON, self.disable_blocking)  # Событие - Отключить блокировку
        # События при нажатии кнопок в тулбаре
        self.Bind(wx.EVT_TOOL, self.on_run_log, self.btn_tool_log)
        self.Bind(wx.EVT_TOOL, self.on_run_timer, self.btn_tool_timer)
        self.Bind(wx.EVT_TOOL, self.on_run_monitor, self.btn_tool_monitor)
        self.Bind(wx.EVT_TOOL, self.on_run_clear_data, self.btn_tool_clear_data)
        self.Bind(wx.EVT_TOOL, self.on_run_unblock, self.btn_tool_run_unblock_usr)
        self.Bind(wx.EVT_TOOL, self.on_run_info, self.btn_tool_info)
        self.Bind(wx.EVT_TOOL, self.on_block_interface, self.btn_tool_block_interface)
        self.Bind(wx.EVT_TOOL, self.on_unblock_interface, self.btn_tool_unblock_interface)
        # END ---------------------------------------------

    # Обработчики событий
    def on_close(self, event):
        """Обработчик закрытия программы"""
        # Ожидаем ответа от пользователя
        dlg = WndCloseApp(self)
        result = dlg.ShowModal()  # Показать диалог с паролем

        # Если пользователь нажал "OK", закрываем все приложение
        if result == wx.ID_OK:
            print(2222)
            print("self.remaining_time:", self.remaining_time)
            # Если время больше ноля и имя пользователя не пустое
            if self.remaining_time > 0 and len(self.username_blocking) >= 1:
                # Запись времени в файл
                function.update_json("remaining_time", self.remaining_time - self.elapsed_time)
            # Если время равно 0
            elif self.remaining_time == 0:
                # Удаляем значение времени если таймер не активен
                function.update_json("remaining_time", 0)
                # Удаляем значение с именем пользователя для блокировки
                function.update_json("username_blocking", "")
            # Если время больше ноля, но имя пустое
            elif self.remaining_time > 0 and len(self.username_blocking) == 0:
                # Очищаем время если таймер не активен
                function.update_json("remaining_time", 0)
                # Сбрасываем поле с временем на 0
                self.input_time.SetSelection(0)

            # При закрытии убираем иконку из трея
            self.tray_icon.RemoveIcon()
            self.tray_icon.Destroy()

            self.Destroy()  # Закрывает основное окно, завершая приложение
            # Завершаем процесс (закрытие программы)
            sys.exit()
        # Если пользователь нажал "Отмена", просто закрываем диалог
        elif result == wx.ID_CANCEL:
            dlg.Destroy()  # Закрываем только диалоговое окно и продолжаем работу

        # Не даем закрыть окно, если нажали "Отмена"
        event.Veto()

    def on_input_changed(self, event):
        """
        Обработчик события выбора имени пользователя и времени
        """
        # =============== Получаем значения из полей ввода ================
        # Имя пользователя получаем из поля выбора и записываем в файл данных
        username_choice = self.input_username.GetValue()  # Получаем имя пользователя для блокировки
        print("Произошло событие в поле выбора пользователя:", username_choice)
        # Записываем имя пользователя для блокировки в файл данных.
        function.update_json("username_blocking", username_choice)
        # Обновляем атрибут в классе
        self.username_blocking = function.read_json("username_blocking")

        # Время блокировки получаем из поля выбора и записываем в файл данных переведя в секунды
        time_choice = int(self.input_time.GetValue()) * 60  # TODO Перевести значение в часы после разработки (*3600)
        # Записывает выбранное время для блокировки в файл данных.
        function.update_json("remaining_time", time_choice)
        # Обновляем атрибут в классе
        self.remaining_time = function.read_json("remaining_time")

        # Получаем данные о сессии
        session_id = function.get_session_id_by_username(self.username_blocking)

        # ==========================================================================
        # Проверяем запущена ли сессия искомого пользователя если нет стираем данные
        if function.get_session_id_by_username(self.username_blocking) is None:
            self.input_time.Disable()  # Отключаем поле выбора времени для блокировки
            self.btn_disable_blocking.Disable()  # Отключаем кнопку - Отключить блокировку

            # Выводим сообщение что-бы выбранный пользователь зашел в систему (сессию)
            dialog = wx.MessageDialog(self,
                                      _(f"Выбранный пользователь: {self.username_blocking} не вошел в свой аккаунт "
                                        f"Windows.\nРЕШЕНИЕ:\n"
                                        f"1 - Нужно зайти в его аккаунт.\n"
                                        f"2 - Запустить программу от имени АДМИНИСТРАТОРА\n"
                                        f"3 - Провести процедуру настройки блокировки снова."
                                        ),
                                      _("Предупреждение"),
                                      wx.ICON_WARNING
                                      )
            dialog.ShowModal()
            dialog.Destroy()

            # Сбрасываем выбор пользователя
            self.input_username.SetSelection(-1)  # Сбрасываем поле имени
            function.update_json("username_blocking", "")  # Стираем имя пользователя в файле
            self.username_blocking = function.read_json("username_blocking")  # Обновляем атрибут имени пользователя
            # Сбрасываем выбор времени
            self.input_time.SetSelection(0)  # Обнуляем время в поле
            function.update_json("remaining_time", 0)  # Стираем значение времени в файле
            self.remaining_time = function.update_json("remaining_time", 0)  # Обновляем атрибут времени блокировки
        else:
            self.input_time.Enable()  # Активируем поле выбора времени
            self.btn_disable_blocking.Enable()  # Активируем кнопку - Отключить блокировку

        # Проверяем, указаны ли пользователь и время и запущена ли сессия.
        if self.input_username.GetValue() and int(time_choice) > 0 and session_id is not None:
            self.btn_ok.Enable()  # Активируем кнопку OK, если значения корректные
            self.input_time.Enable()  # Активируем поле с временем для блокировки
        else:
            self.btn_ok.Disable()  # Деактивируем кнопку, если значения некорректные или пустые

    def start_blocking(self, event):
        """
        Обработчик запуска задания блокировки. Кнопка ОК
        """
        username = self.input_username.GetValue()  # Получаем имя пользователя для блокировки
        hours = int(self.input_time.GetValue())  # Получаем время для таймера из поля выбора времени
        self.remaining_time = int(hours * 60)  # TODO Перевести значение в часы после разработки (*3600)

        # Настройка таймера
        self.elapsed_time = 0  # Инициализируем прошедшее время
        self.gauge.SetRange(self.remaining_time)  # Передаем время блокировки в статус строку
        self.gauge.SetValue(0)  # Начальное значение шкалы
        self.timer.Start(1000)  # Запуск таймера с интервалом 1 секунда
        self.btn_ok.Disable()  # Блокируем кнопку OK, пока таймер работает
        self.input_username.Disable()  # Блокируем поле имени пользователя
        self.input_time.Disable()  # Блокируем поле выбора времени блокировки

        if username == function.username_session():
            dialog = wx.MessageDialog(self,
                                      _("Внимание убедитесь что вы выбрали не АДМИНИСТРАТОРА !!!\n"
                                        "Только АДМИНИСТРАТОР может снять блокировку !!!.\n"
                                        "В противном случае блокировку уже не снять.\n"
                                        "РЕШЕНИЕ - ПЕРЕУСТАНОВКА WINDOWS !!!"
                                        ),
                                      _("Предупреждение"),
                                      wx.ICON_WARNING
                                      )
            dialog.ShowModal()
            dialog.Destroy()

    def run_on_timer(self, event):
        """
        Обработчик таймера.
        """
        # Сохраняем имя пользователя для блокировки в файл
        function.update_json("username_blocking", self.username_blocking)

        if self.elapsed_time < self.remaining_time:
            self.elapsed_time += 1  # Увеличиваем прошедшее время
            self.gauge.SetValue(self.elapsed_time)  # Обновляем значение шкалы по мере увеличения времени
            # Сохраняем оставшееся время в файл при каждом тике таймера
            function.update_json("remaining_time", self.remaining_time - self.elapsed_time)
            # Обновление значения текста в таймере главного окна (01:10:23)
            self.timer_time.SetLabel(self.seconds_to_hms(self.remaining_time - self.elapsed_time))

        else:
            self.timer.Stop()  # Останавливаем таймер, когда время истекло

            # =============== Логика блокировки учетной записи и рабочего стола.
            # TODO Запускаем блокировку ==========================
            username = self.username_blocking  # Получаем имя пользователя для блокировки
            session_data = function.get_session_id_by_username(username)  # Данные о сессии
            id_session_username = int(*(id for id in session_data if id.isdigit()))  # ID сессии
            function.blocking(username, id_session_username)  # Запуск
            # ====================== END ==========================

            # После того как отработала блокировка пользователя настраиваем интерфейс и обновляем данные.
            self.gauge.SetValue(0)  # Обнуляем статус строку

            function.update_json("remaining_time", 0)  # Удаляем значение времени в файле.
            function.update_json("username_blocking", "")  # Удаляем значение имени пользователя в файле.

            self.input_username.SetSelection(-1)  # Стираем значение в поле имя пользователя.
            self.input_username.Enable()  # Активируем поле выбора имени
            self.input_time.SetSelection(0)  # Стираем значение в поле выбора времени для блокировки
            self.input_time.Disable()  # Отключаем поле выбора времени
            self.timer_time.SetLabel("00:00:00")  # Обновляем время в поле таймера
            self.btn_disable_blocking.Disable()  # Отключаем кнопку отл=ключения блокировки

    def disable_blocking(self, event):
        """
        Обработчик отключение блокировки
        """
        username = self.username_blocking
        print("def disable_blocking:", username)

        # Отмена блокировки если имя пользователя пустое
        if username == "":
            dialog = wx.MessageDialog(self,
                                      _("Вы не указали пользователя для отключения блокировки."),
                                      _("Предупреждение"),
                                      wx.ICON_WARNING
                                      )
            dialog.ShowModal()
        else:
            self.timer.Stop()  # Останавливаем таймер
            self.gauge.SetValue(0)  # Стираем статус заполненности таймера

            # Стираем значение в поле имя пользователя.
            self.input_username.SetSelection(-1)
            # Очищаем значение имени пользователя в файле
            function.update_json("username_blocking", "")  # Удаляем значение с именем пользователя для блокировки.

            # Стираем значение в поле выбора времени для блокировки
            self.input_time.SetSelection(0)
            # Очищаем значение времени в файле
            function.update_json("remaining_time", 0)  # Удаляем значение времени в файле.
            # Стираем значение атрибута времени для бокировки в классе
            self.remaining_time = function.read_json("remaining_time")

            # Сбрасываем значение времени в поле - "Осталось времени до блокировки:"
            self.timer_time.SetLabel("00:00:00")
            self.enable_fields()

            # Сообщение
            dialog = wx.MessageDialog(self,
                                      _(f"(1)Пользователь - {username} - разблокирован"),
                                      _("Предупреждение"),
                                      wx.ICON_WARNING
                                      )
            dialog.ShowModal()

    def disable_fields(self):
        """Функция отключения полей для ввода"""
        # Деактивируем все поля главного приложения
        self.input_username.Disable()  # Поле имени пользователя для блокировки
        self.input_time.Disable()  # Поле времени
        self.gauge.Disable()  # Поле прогресса времени
        self.btn_disable_blocking.Disable()  # Кнопка - Отключить блокировку
        self.btn_ok.Disable()  # Кнопка ОК
        # Деактивируем кнопки в тулбаре
        self.tool_bar.EnableTool(self.btn_tool_log.GetId(), False)
        self.tool_bar.EnableTool(self.btn_tool_timer.GetId(), False)
        self.tool_bar.EnableTool(self.btn_tool_monitor.GetId(), False)
        self.tool_bar.EnableTool(self.btn_tool_clear_data.GetId(), False)
        self.tool_bar.EnableTool(self.btn_tool_run_unblock_usr.GetId(), False)
        self.tool_bar.EnableTool(self.btn_tool_info.GetId(), False)

        self.tool_bar.EnableTool(self.btn_tool_unblock_interface.GetId(), False)
        self.tool_bar.EnableTool(self.btn_tool_block_interface.GetId(), False)

    def enable_fields(self):
        """Функция включения (активации) полей для ввода"""
        # Активируем поля если пароль совпал.
        self.input_username.Enable()  # Поле имени пользователя для блокировки
        self.gauge.Enable()  # Поле прогресса времени
        # Активируем кнопки в тулбаре
        self.tool_bar.EnableTool(self.btn_tool_log.GetId(), True)
        self.tool_bar.EnableTool(self.btn_tool_timer.GetId(), True)
        self.tool_bar.EnableTool(self.btn_tool_monitor.GetId(), True)
        self.tool_bar.EnableTool(self.btn_tool_clear_data.GetId(), True)
        self.tool_bar.EnableTool(self.btn_tool_run_unblock_usr.GetId(), True)
        self.tool_bar.EnableTool(self.btn_tool_info.GetId(), True)

        self.tool_bar.EnableTool(self.btn_tool_unblock_interface.GetId(), True)
        self.tool_bar.EnableTool(self.btn_tool_block_interface.GetId(), True)
        self.tool_bar.Enable(True)

    def enable_fields_if_have_time(self):
        """
        Функция включения (активации) полей для ввода.
        Если было ОСТАТОЧНОЕ время в файле с данными.
        """
        self.input_username.Disable()  # Поле выбора пользователя
        self.gauge.Enable()  # Поле прогресса времени
        self.btn_disable_blocking.Enable()  # Кнопка - Отключить блокировку
        self.tool_bar.EnableTool(self.btn_tool_clear_data.GetId(), True)  # Активируем кнопку тулбара Стереть все

    def seconds_to_hms(self, seconds):
        """
        Преобразует количество секунд в строку формата часы:минуты:секунды.

        :param seconds: Количество секунд (целое число).
        :return: Строка формата "часы:минуты:секунды".
        """
        # Вычисляем количество часов, минут и секунд
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60

        # Форматируем результат с ведущими нулями
        return f"{hours:02}:{minutes:02}:{secs:02}"

    # Обработчики тулбара
    def on_run_log(self, event):
        """Запуск просмотра логов программы"""
        try:
            os.startfile(path_log_file)  # Открываем файл в ассоциированном приложении (обычно Блокнот)
        except Exception as e:
            wx.MessageBox(f"Не удалось открыть файл: {str(e)}", "Ошибка", wx.OK | wx.ICON_ERROR)

    def on_run_timer(self, event):
        """Запуск окна таймера"""
        try:
            # Запускаем .exe файл через subprocess
            subprocess.Popen([path_timer_exe])
        except Exception as e:
            # Выводим сообщение об ошибке, если не удалось запустить приложение
            wx.MessageBox(f"{path_timer_exe}: {str(e)}", "Ошибка", wx.OK | wx.ICON_ERROR)
            # Записываем лог
            self.log_error(f"{path_timer_exe} {str(e)}")

    def on_run_monitor(self, event):
        """Запуск программы мониторинга """
        try:
            # Запускаем .exe файл через subprocess
            subprocess.Popen([path_monitor_exe])
        except Exception as e:
            # Выводим сообщение об ошибке, если не удалось запустить приложение
            wx.MessageBox(f"{path_monitor_exe} {str(e)}", "Ошибка", wx.OK | wx.ICON_ERROR)
            # Записываем лог
            self.log_error(f"{path_monitor_exe} {str(e)}")

    def on_run_unblock(self, event):
        """Запуск программы для разблокировки пользователя"""
        try:
            # Запускаем .exe файл через subprocess
            subprocess.Popen([path_unblock_usr_exe])
        except Exception as e:
            # Выводим сообщение об ошибке, если не удалось запустить приложение
            wx.MessageBox(f"{path_unblock_usr_exe} {str(e)}", "Ошибка", wx.OK | wx.ICON_ERROR)
            # Записываем лог
            self.log_error(f"{path_unblock_usr_exe} {str(e)}")

    def on_run_clear_data(self, event):
        """
        Очистка данных в полях и файле с данными.
        Полный сброс задания блокировщика.
        PS.
        НЕ СНИМАЕТ БЛОКИРОВКУ С ПОЛЬЗОВАТЕЛЯ
        """
        # Останавливаем таймер (если он работает)
        self.timer.Stop()
        # Сбрасываем статус строку таймера (прошедшее время)
        self.gauge.SetValue(0)  # Начальное значение шкалы
        # Стираем значение в поле имя пользователя.
        self.input_username.SetSelection(-1)
        # Стираем значение в поле выбора времени для блокировки
        self.input_time.SetSelection(0)
        # Сбрасываем значение времени в поле - "Осталось времени до блокировки:"
        self.timer_time.SetLabel("00:00:00")
        # Очищаем содержимое времени в файле
        function.update_json("remaining_time", 0)  # Записываем значение времени 0 в файл
        # Очищаем содержимое имени пользователя в файле
        function.update_json("username_blocking", "")  # Записываем пустую строку в файл

        # Активируем поле выбора имени пользователя для блокировки
        self.input_username.Enable()
        # Отключаем поле выбора времени блокировки
        self.input_time.Disable()
        # Отключаем кнопку - Отключить блокировку
        self.btn_disable_blocking.Disable()
        # Отключаем кнопку ОК
        self.btn_ok.Disable()

        # Вывод сообщения об успешной очистке
        wx.MessageBox(f"Все настройки программы сброшены !", "СБРОС ДАННЫХ", wx.OK | wx.ICON_INFORMATION)

    def on_run_info(self, event):
        """Запуск окна справки"""
        # TODO Возможно нужно открывать в отдельном потоке от основной программы....не уверен
        doc_app = DocWindow(None)
        doc_app.Show()

    def on_block_interface(self, event):
        """Блокировка интерфейса при нажатии кнопки - Заблокировать интерфейс"""
        # Блокируем все поля окна
        self.disable_fields()
        # Но оставляем одну кнопку активной - "Разблокировать интерфейс"
        self.tool_bar.EnableTool(self.btn_tool_unblock_interface.GetId(), True)

    def on_unblock_interface(self, event):
        """Разблокировка интерфейса при попытке нажать в тулбаре на кнопку - Разблокировать интерфейс"""
        # Отображаем окно ввода пароля
        dlg = WndPass(None)
        dlg.ShowModal()

        # Активируем все поля для разблокировки если пароль совпал
        self.enable_fields()

    def log_error(self, message):
        """Логирование ошибок в файл."""
        try:
            with open(path_log_file, 'a', encoding="utf-8") as log_file:
                log_file.write(f"CPG({time.strftime('%Y-%m-%d %H:%M:%S')}) - "
                               f"{message}\n==================\n"
                               )
        except Exception as e:
            print(f"(1)Ошибка при записи лога в файл: {str(e)}")
            ctypes.windll.user32.MessageBoxW(None, f"Ошибка при записи в файл лога:\n{str(e)}", "ОШИБКА", 0)

    # =============================================================================================================


def main():
    # Запускаем приложение как администратор
    function.run_as_admin()

    # ------- Создание мьютекса -------
    # Проверка кода ошибки
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, MUTEX_NAME)
    error_code = ctypes.windll.kernel32.GetLastError()
    if error_code == 183:
        ctypes.windll.user32.MessageBoxW(None, f"Приложение Child PC Guard уже запущено.", "ПРЕДУПРЕЖДЕНИЕ", 0)
        # Закрываем дескриптор мьютекса, так как он не нужен
        ctypes.windll.kernel32.CloseHandle(mutex)
        return
    elif error_code == 5:  # ERROR_ACCESS_DENIED
        ctypes.windll.user32.MessageBoxW(None, "Доступ к мьютексу запрещен.", "ОШИБКА", 0)
        ctypes.windll.kernel32.CloseHandle(mutex)
        return
    elif error_code != 0:
        ctypes.windll.user32.MessageBoxW(None, f"Неизвестная ошибка:\n{error_code}", "ОШИБКА", 0)
        # Закрываем дескриптор мьютекса
        ctypes.windll.kernel32.CloseHandle(mutex)
        return
    # -------------- END ---------------

    # Создаем папки и файлы с данными для работы приложения в местах допуска системы windows 10/11
    function.function_to_create_path_data_files()

    username_blocking = function.read_json("username_blocking")  # Имя пользователя для блокировки из файла
    remaining_time = function.read_json("remaining_time")  # Время задаваемой блокировки из файла
    # Выводим заставку
    main_splash()

    # Инициализируем главное окно в случае продолжения отсчета программой времени из файла данных
    app = wx.App(False)
    main_frame = Window(None)
    # Деактивируем все поля главного приложения
    main_frame.disable_fields()

    # Создаем и отображаем окно ввода пароля
    dlg = WndPass(None)
    dlg.ShowModal()

    # Проверяем если есть остаточное время в файле с данными то активируем необходимые поля главного приложения
    if username_blocking and remaining_time > 0:
        print("=========================")
        main_frame.enable_fields_if_have_time()
    #  Иначе это чистый запуск активируем необходимое
    else:
        # Активируем все поля если пароль совпал
        main_frame.enable_fields()

    if dlg.password_check:
        main_frame.Show()

    app.MainLoop()

    # Закрываем дескриптор мьютекса, когда приложение завершает работу
    ctypes.windll.kernel32.CloseHandle(mutex)


if __name__ == "__main__":
    main()

# TODO !!! ВАЖНО при работе окна таймера для пользователя периодично выводится ошибка при считывании времени.
