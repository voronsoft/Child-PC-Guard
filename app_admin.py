"""
Главное приложения CPG
"""

import ctypes
import os
import sys

import wx
import wx.xrc

import app_wnd_add_app_defender
import app_wind_documentation
import app_wnd_input_first_pass
import config_localization
import function
from add_task_schedule import run_add_task
from app_admin_event_handlers import EventHandlers
from app_wind_exit_prog import WndCloseApp
from app_wind_splash_screen import main_splash
from app_wind_tray_icon import TrayIcon
from config_app import FOLDER_IMG

# Подключаем локализацию
_ = config_localization.setup_locale(function.read_data_json("language"))

# Имя мьютекса (должно быть уникальным)
MUTEX_NAME_CPG = "Global\\Child_PC_Guard"


###########################################################################
## Class Window
## Класс окна основного приложения
###########################################################################
class Window(wx.Frame):
    """Класс окна основного приложения"""

    def __init__(self, parent):
        wx.Frame.__init__(
                self,
                parent,
                id=wx.ID_ANY,
                title=_("Child PC Guard - АДМИНИСТРАТОР"),
                pos=wx.DefaultPosition,
                size=wx.DefaultSize,
                style=wx.DEFAULT_FRAME_STYLE & ~wx.MAXIMIZE_BOX | wx.TAB_TRAVERSAL,
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
        # Создаем экземпляр обработчиков и передаем ссылку на основной класс
        self.event_handlers = EventHandlers(self)

        self.timer = wx.Timer(self)  # Таймеp
        self.username_blocking = function.read_data_json(
                "username_blocking"
        )  # Имя пользователя для блокировки из файла
        self.remaining_time = function.read_data_json("remaining_time")  # Время задаваемой блокировки из файла
        self.elapsed_time = 0  #
        self.passwort_registry = ""
        # Определяем режим работы приложения, если не АДМИНИСТРАТОР фон красный окно не активно
        self.mode_run_app = function.check_mode_run_app()
        if self.mode_run_app != "admin":
            self.SetBackgroundColour(wx.Colour(255, 160, 160))  # Красный фон
            self.SetTitle(_("Child PC Guard - ПОЛЬЗОВАТЕЛЬ"))  # Заголовок

        # ============================ END =============================
        # Создаем иконку в системном трее
        self.tray_icon = TrayIcon(self)

        # Тулбар =======================================================
        self.tool_bar = self.CreateToolBar(wx.TB_HORIZONTAL, wx.ID_ANY)
        self.tool_bar.SetToolSeparation(5)
        self.tool_bar.SetFont(
                wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Segoe UI")
        )
        self.tool_bar.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))

        self.tool_bar.AddStretchableSpace()  # Вставляем гибкое пространство
        self.btn_tool_lang = self.tool_bar.AddTool(
                wx.ID_ANY,
                _("Lang"),
                wx.Bitmap(os.path.join(FOLDER_IMG, "language.ico"), wx.BITMAP_TYPE_ANY),
                wx.NullBitmap,
                wx.ITEM_NORMAL,
                _("Lang"),
                _("Выбор языка интерфейса"),
                None,
        )
        self.tool_bar.AddStretchableSpace()  # Вставляем гибкое пространство
        self.btn_tool_log = self.tool_bar.AddTool(
                wx.ID_ANY,
                _("Логи"),
                wx.Bitmap(os.path.join(FOLDER_IMG, "logs.ico"), wx.BITMAP_TYPE_ANY),
                wx.NullBitmap,
                wx.ITEM_NORMAL,
                _("Логи"),
                _("Просмотр логов программы"),
                None,
        )
        self.tool_bar.AddStretchableSpace()  # Вставляем гибкое пространство
        self.btn_tool_timer = self.tool_bar.AddTool(
                wx.ID_ANY,
                _("Таймер"),
                wx.Bitmap(os.path.join(FOLDER_IMG, "time.ico"), wx.BITMAP_TYPE_ANY),
                wx.NullBitmap,
                wx.ITEM_NORMAL,
                _("Таймер"),
                _("Открыть окно таймера"),
                None,
        )

        self.tool_bar.AddStretchableSpace()  # Вставляем гибкое пространство
        self.btn_tool_clear_data = self.tool_bar.AddTool(
                wx.ID_ANY,
                _("Очистить"),
                wx.Bitmap(os.path.join(FOLDER_IMG, "clear.ico"), wx.BITMAP_TYPE_ANY),
                wx.NullBitmap,
                wx.ITEM_NORMAL,
                _("Очистить все"),
                _("Удаляет все данные задания для блокировки. БЛОКИРОВКУ НЕ ОТКЛЮЧАЕТ"),
                None,
        )
        self.tool_bar.AddStretchableSpace()  # Вставляем гибкое пространство
        self.btn_tool_run_unblock_usr = self.tool_bar.AddTool(
                wx.ID_ANY,
                _(r"Разблокировать"),
                wx.Bitmap(os.path.join(FOLDER_IMG, "unlock.ico"), wx.BITMAP_TYPE_ANY),
                wx.NullBitmap,
                wx.ITEM_NORMAL,
                _("Разблокировать пользователя"),
                _("Открывает окно разблокировки пользователя"),
                None,
        )
        self.tool_bar.AddStretchableSpace()  # Вставляем гибкое пространство
        self.btn_tool_info = self.tool_bar.AddTool(
                wx.ID_ANY,
                _("Справка"),
                wx.Bitmap(os.path.join(FOLDER_IMG, "doc.ico"), wx.BITMAP_TYPE_ANY),
                wx.NullBitmap,
                wx.ITEM_NORMAL,
                _("Справка"),
                _("Открывает окно по использованию программы"),
                None,
        )
        self.tool_bar.AddStretchableSpace()  # Вставляем гибкое пространство
        self.btn_tool_bot = self.tool_bar.AddTool(
                wx.ID_ANY,
                _("Оповещение"),
                wx.Bitmap(os.path.join(FOLDER_IMG, "telegram.ico"), wx.BITMAP_TYPE_ANY),
                wx.NullBitmap,
                wx.ITEM_NORMAL,
                _("Оповещение"),
                _("Открывает окно для настройки оповещения через Telegram"),
                None,
        )
        self.tool_bar.AddStretchableSpace()  # Вставляем гибкое пространство

        self.btn_tool_unblock_interface = self.tool_bar.AddTool(
                wx.ID_ANY,
                _("Разблокировать интерфейс"),
                wx.Bitmap(os.path.join(FOLDER_IMG, "open.ico")),
                wx.NullBitmap,
                wx.ITEM_RADIO,
                _("Разблокировать интерфейс"),
                _("Разблокировать интерфейс"),
                None,
        )
        self.btn_tool_block_interface = self.tool_bar.AddTool(
                wx.ID_ANY,
                _("Заблокировать интерфейс"),
                wx.Bitmap(os.path.join(FOLDER_IMG, "close.ico")),
                wx.NullBitmap,
                wx.ITEM_RADIO,
                _("Заблокировать интерфейс"),
                _("Блокировка интерфейса"),
                None,
        )

        self.tool_bar.AddStretchableSpace()
        self.tool_bar.Realize()
        # ============================ END Туллбар =======================
        # Исходя из режима с какими правами запущена программа меняется фон окна приложения.

        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.SetMinSize(wx.Size(-1, -1))

        sizer_top = wx.BoxSizer(wx.HORIZONTAL)

        self.txt_input_username = wx.StaticText(
                self, wx.ID_ANY, _("Укажите пользователя для блокировки: "), wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.txt_input_username.Wrap(-1)
        sizer_top.Add(self.txt_input_username, 0, wx.ALL, 5)

        # Получаем список пользователей и создаем ComboBox
        users = function.get_users()
        # Исключаем из списка пользователя который под защитой (указан в БД)
        user_list = [user for user in users if user != function.read_data_json("protected_user")]

        if not user_list:
            user_list = [_("----")]
        self.input_username = wx.ComboBox(
                self,
                wx.ID_ANY,
                wx.EmptyString,
                wx.DefaultPosition,
                wx.Size(150, -1),
                choices=user_list,
                style=wx.CB_DROPDOWN | wx.CB_READONLY,
        )
        sizer_top.Add(self.input_username, 0, wx.ALL, 5)
        sizer_main.Add(sizer_top, 0, wx.EXPAND, 5)

        self.staticline = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        sizer_main.Add(self.staticline, 0, wx.EXPAND | wx.ALL, 5)

        bSizer6 = wx.BoxSizer(wx.VERTICAL)

        sizer_main.Add(bSizer6, 1, wx.EXPAND, 5)

        sizer_top = wx.BoxSizer(wx.HORIZONTAL)

        self.txt_timer = wx.StaticText(
                self, wx.ID_ANY, _("Укажите время для блокировки: "), wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.txt_timer.Wrap(-1)
        sizer_top.Add(self.txt_timer, 0, wx.ALL, 5)

        combo_box_choices = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

        self.input_time = wx.ComboBox(
                self, wx.ID_ANY, _("0"), wx.DefaultPosition, wx.DefaultSize, combo_box_choices, wx.CB_READONLY
        )
        # Устанавливаем начальное значение временем на 0
        self.input_time.SetSelection(0)

        self.input_time.SetMinSize(wx.Size(202, -1))

        sizer_top.Add(self.input_time, 0, wx.ALL, 5)

        self.txt_2 = wx.StaticText(self, wx.ID_ANY, _("час (0 отключено)"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.txt_2.Wrap(-1)

        sizer_top.Add(self.txt_2, 0, wx.ALL, 5)

        sizer_main.Add(sizer_top, 0, wx.EXPAND, 5)

        self.staticline = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        sizer_main.Add(self.staticline, 0, wx.EXPAND | wx.ALL, 5)

        sizer_center1 = wx.BoxSizer(wx.VERTICAL)
        self.txt_3 = wx.StaticText(
                self, wx.ID_ANY, _("Осталось времени до блокировки:"), wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.txt_3.Wrap(-1)

        sizer_center1.Add(self.txt_3, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.timer_time = wx.StaticText(self, wx.ID_ANY, _("00:00:00"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.timer_time.Wrap(-1)
        sizer_center1.Add(self.timer_time, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.gauge = wx.Gauge(self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL)
        sizer_center1.Add(self.gauge, 0, wx.ALL | wx.EXPAND, 5)
        sizer_main.Add(sizer_center1, 1, wx.ALL | wx.EXPAND, 5)

        sizer_center2 = wx.BoxSizer(wx.VERTICAL)
        self.btn_disable_blocking = wx.Button(
                self, wx.ID_ANY, _("Отключить блокировку"), wx.DefaultPosition, wx.DefaultSize, 0
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
        # Логика если есть остаточное время в файле.
        # Загрузка оставшегося времени из файла, если оно есть
        # Если есть остаточное время и имя в файле данных data.json
        if self.remaining_time > 0 and len(self.username_blocking) >= 1:
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
            function.update_data_json("username_blocking", "")
            self.username_blocking = function.read_data_json("username_blocking")
        # Если время есть, а имени нет
        elif self.remaining_time > 0 and len(self.username_blocking) == 0:
            # Очищаем имя пользователя для блокировки в файле
            function.update_data_json("username_blocking", "")
            # Очищаем время блокировки в файле
            function.update_data_json("remaining_time", 0)
        # END - логика если есть остаточное время в файле.
        # -------------------------------------------------

        # Подключаемые события в программе ----------------
        # Событие при выборе имени пользователя
        self.input_username.Bind(wx.EVT_TEXT, self.event_handlers.on_input_changed)
        # Событие при выборе времени для блокировки
        self.input_time.Bind(wx.EVT_COMBOBOX, self.event_handlers.on_input_changed)
        # Событие, при запуске таймера
        self.Bind(wx.EVT_TIMER, self.event_handlers.run_on_timer, self.timer)
        # Событие, закрытия окна
        self.Bind(wx.EVT_CLOSE, self.on_close)
        # Событие, при нажатии OK (запуск задания)
        self.btn_ok.Bind(wx.EVT_BUTTON, self.event_handlers.start_blocking)
        # Событие - Отключить блокировку
        self.btn_disable_blocking.Bind(wx.EVT_BUTTON, self.event_handlers.disable_blocking)
        # События при нажатии кнопок в тулбаре ------------
        # Выбор языка
        self.Bind(wx.EVT_TOOL, self.event_handlers.on_lang, self.btn_tool_lang)
        # Просмотр логов
        self.Bind(wx.EVT_TOOL, self.event_handlers.on_run_log, self.btn_tool_log)
        # Запуск окна таймера
        self.Bind(wx.EVT_TOOL, self.event_handlers.on_run_timer, self.btn_tool_timer)
        # Стирает все данные приложения
        self.Bind(wx.EVT_TOOL, self.event_handlers.on_run_clear_data, self.btn_tool_clear_data)
        # Запуск приложения разблокировки пользователя
        self.Bind(wx.EVT_TOOL, self.event_handlers.on_run_unblock, self.btn_tool_run_unblock_usr)
        # Справка о программе
        self.Bind(wx.EVT_TOOL, self.event_handlers.on_run_info, self.btn_tool_info)
        # Запуск приложения настройки оповещения через Telegram
        self.Bind(wx.EVT_TOOL, self.event_handlers.on_run_bot, self.btn_tool_bot)
        # Блокировка интерфейса
        self.Bind(wx.EVT_TOOL, self.event_handlers.on_block_interface, self.btn_tool_block_interface)
        # Разблокировать интерфейс
        self.Bind(wx.EVT_TOOL, self.event_handlers.on_unblock_interface, self.btn_tool_unblock_interface)
        # END ---------------------------------------------

    # Обработчики событий (смотреть файл - app_admin_event_handlers.py)
    def on_close(self, event):
        """Обработчик закрытия программы"""
        # Ожидаем ответа от пользователя
        dlg = WndCloseApp(self)
        result = dlg.ShowModal()  # Показать диалог с паролем

        # Если пользователь нажал "OK", закрываем все приложение
        if result == wx.ID_OK:
            # ------------- Останавливаем БОТ ---------------
            function.kill_program_by_name("run_bot_telegram.exe")
            # -----------------------------------------------

            # print("self.remaining_time:", self.remaining_time)
            # Если время больше ноля и имя пользователя не пустое
            if self.remaining_time > 0 and len(self.username_blocking) >= 1:
                # Запись времени в файл
                function.update_data_json("remaining_time", self.remaining_time - self.elapsed_time)
            # Если время равно 0
            elif self.remaining_time == 0:
                # Удаляем значение времени если таймер не активен
                function.update_data_json("remaining_time", 0)
                # Удаляем значение с именем пользователя для блокировки
                function.update_data_json("username_blocking", "")
            # Если время больше ноля, но имя пустое
            elif self.remaining_time > 0 and len(self.username_blocking) == 0:
                # Очищаем время если таймер не активен
                function.update_data_json("remaining_time", 0)
                # Сбрасываем поле с временем на 0
                self.input_time.SetSelection(0)

            # При закрытии убираем иконку из трея
            self.tray_icon.RemoveIcon()
            self.tray_icon.Destroy()

            self.Destroy()  # Закрывает основное окно, завершая приложение

            # Проверяем мьютекс, созданный в другом месте приложения
            mutex = ctypes.windll.kernel32.OpenMutexW(0x00100000, False, MUTEX_NAME_CPG)  # SYNCHRONIZE
            # Закрываем дескриптор мьютекса
            ctypes.windll.kernel32.CloseHandle(mutex)

            function.send_bot_telegram_message(_("Программа CPG была выключена"))

            # Завершаем процесс (закрытие программы)
            sys.exit()
        # Если пользователь нажал "Отмена", просто закрываем диалог
        elif result == wx.ID_CANCEL:
            dlg.Destroy()  # Закрываем только диалоговое окно и продолжаем работу


def main_app():
    """Функция запуска главного приложения"""
    # Запускаем приложение как администратор
    function.run_as_admin()
    print("01")
    # ------- Проверка кода ошибки на запуск приложения в единственном числе -------
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, MUTEX_NAME_CPG)
    error_code = ctypes.windll.kernel32.GetLastError()
    print("02")
    function.process_mutex_error(error_code, mutex)
    # ------------------------------------ END -------------------------------------

    # Запуск окна соглашения о добавлении программы как доверенный источник.
    # Для отключения блокировки системой защиты от вирусов.
    app_wnd_add_app_defender.run_main_add_def_app()
    print(1)
    # Создаем папки и файлы с данными для работы приложения если они не существуют
    function.function_to_create_path_data_files()
    print(2)
    # Получаем пароль из реестра
    password_from_registry = function.get_password_from_registry()
    print(3)
    # Получаем пользователей системы
    user_list_os = function.get_users()
    if len(user_list_os) <= 1:
        # Выводим окно предупреждения, что в системе должно быть как минимум 2 пользователя
        # (1 админ 1 пользователь/админ)
        function.show_message_with_auto_close(
                _(
                        "В системе всего один пользователь, приложение не будет работать!!\n"
                        "Необходимо, что-бы в системе было два пользователя.\n"
                        "1- Администратор\n2- Пользователь/Администратор\n"
                        "Необходимо создать второго пользователя.\n"
                        "После этого программа запустится."
                ),
                _("ОШИБКА"),
                15,
        )

        # Закрываем приложение для защиты
        ctypes.windll.kernel32.CloseHandle(mutex)  # Закрываем дескриптор мьютекса
        sys.exit(0)
    print(4)
    # Если пароля нет в реестре, то запускаем приложение как в первый раз с вводом будущего пароля для приложения
    if not password_from_registry:
        # Выводим описание о программе - Документация
        app_wind_documentation.run_wind_doc()
        # Вывод окна для настройки приложения
        app_wnd_input_first_pass.main()
        # Вывод заставки программы
        main_splash()
        # При первом запуске активируем добавление задачи в 'Планировщик заданий'
        run_add_task()
    print(5)
    # Запускаем приложение бота
    function.run_program_bot()
    print(6)
    # Инициализируем главное окно
    app = wx.App(False)
    main_frame = Window(None)
    main_frame.event_handlers.disable_fields()
    main_frame.event_handlers.enable_fields_tool_bar()
    print(7)
    main_frame.Show()
    # Основной цикл приложения
    app.MainLoop()
    print(8)
    # Закрываем дескриптор мьютекса
    ctypes.windll.kernel32.CloseHandle(mutex)
    print(9)
    sys.exit(0)


if __name__ == "__main__":

    # Запуск главного приложения
    main_app()
    print(10)