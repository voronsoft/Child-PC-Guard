import wx
import wx.xrc
import gettext
import test_block

_ = gettext.gettext


###########################################################################
## Class Window
###########################################################################

class Window(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self,
                           parent,
                           id=wx.ID_ANY,
                           title=_("Child PC Guard"),
                           pos=wx.DefaultPosition,
                           size=wx.DefaultSize,
                           style=wx.DEFAULT_DIALOG_STYLE
                           )

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Segoe UI"))

        self.username_blocking = test_block.read_json("username_blocking")  # Имя пользователя для блокировки
        # Таймер
        self.timer = wx.Timer(self)  # Таймеp
        self.remaining_time = 0  # Время задаваемой блокировки

        sizer_main = wx.BoxSizer(wx.VERTICAL)

        sizer_main.SetMinSize(wx.Size(600, 400))
        # Устанавливаем иконку для окна
        icon = wx.Icon('img/icon.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

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
        user_list = test_block.get_users()
        print(user_list)
        if not user_list:
            user_list = [_("Пользователи не найдены")]
        self.input_username = wx.ComboBox(self, wx.ID_ANY, choices=user_list, style=wx.CB_DROPDOWN)
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

        combo_boxChoices = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", wx.EmptyString]
        self.combo_box = wx.ComboBox(self, wx.ID_ANY, _("0"), wx.DefaultPosition, wx.DefaultSize, combo_boxChoices, 0)
        self.combo_box.SetSelection(0)

        self.combo_box.SetMinSize(wx.Size(130, -1))

        sizer_top.Add(self.combo_box, 0, wx.ALL, 5)

        self.txt_2 = wx.StaticText(self, wx.ID_ANY, _("час (0 отключено)"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.txt_2.Wrap(-1)

        sizer_top.Add(self.txt_2, 0, wx.ALL, 5)

        sizer_main.Add(sizer_top, 0, wx.EXPAND, 5)

        self.staticline = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        sizer_main.Add(self.staticline, 0, wx.EXPAND | wx.ALL, 5)

        sizer_center1 = wx.BoxSizer(wx.VERTICAL)

        self.txt_3 = wx.StaticText(self,
                                   wx.ID_ANY,
                                   _("Таймер времени."),
                                   wx.DefaultPosition,
                                   wx.DefaultSize,
                                   0
                                   )
        self.txt_3.Wrap(-1)

        sizer_center1.Add(self.txt_3, 0, wx.ALIGN_CENTER | wx.ALL, 5)

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

        sizer_main.Add(sizer_center2, 1, wx.EXPAND, 5)

        sizer_bottom = wx.BoxSizer(wx.HORIZONTAL)

        self.btn_ok = wx.Button(self, wx.ID_ANY, _("OK"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_ok.Disable()  # Деактивируем кнопку
        sizer_bottom.Add(self.btn_ok, 0, wx.ALL, 5)

        self.collapse_window = wx.Button(self, wx.ID_ANY, _("Свернуть окно в трей."), wx.DefaultPosition,
                                         wx.DefaultSize, 0
                                         )
        sizer_bottom.Add(self.collapse_window, 0, wx.ALL, 5)

        sizer_main.Add(sizer_bottom, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.SetSizer(sizer_main)
        self.Layout()
        sizer_main.Fit(self)

        self.Centre(wx.BOTH)

        # ------------------------------------------------
        # TODO логика если есть остаточное время в файле.

        # Загрузка оставшегося времени из файла, если оно есть
        saved_time = test_block.read_json("remaining_time")  # Считываем время из файла
        saved_usr = test_block.read_json("username_blocking")  # Считываем имя пользователя из файла
        print(f"Время из файла - {saved_time} - ({type(saved_time)})")
        print(f"Имя из файла - {saved_usr} - ({type(saved_usr)})")

        if saved_time > 0 and len(self.input_username.GetValue()) > 3:
            self.btn_ok.Disable()

        if saved_time is not None and saved_time > 0:
            # self.btn_ok.Disable()  # Отключаем кнопку
            self.remaining_time = saved_time
            self.elapsed_time = 0
            self.gauge.SetRange(self.remaining_time)
            self.gauge.SetValue(self.elapsed_time)
            self.timer.Start(1000)  # Запускаем таймер, если есть оставшееся время
        else:
            self.remaining_time = 0
        # END - логика если есть остаточное время в файле.
        # ------------------------------------------------

        # Подключаемые события в программе
        self.input_username.Bind(wx.EVT_TEXT, self.on_input_changed)
        self.combo_box.Bind(wx.EVT_COMBOBOX, self.on_input_changed)

        self.Bind(wx.EVT_TIMER, self.run_on_timer, self.timer)  # Событие, при запуске таймера
        self.Bind(wx.EVT_CLOSE, self.on_close)  # Событие, закрытия окна
        self.btn_ok.Bind(wx.EVT_BUTTON, self.start_blocking)  # Событие, при нажатии кнопки OK (запуск задания)
        self.collapse_window.Bind(wx.EVT_BUTTON, self.collapse_program)  # Событие, свернуть окно
        self.btn_disable_blocking.Bind(wx.EVT_BUTTON, self.disable_blocking)  # Событие, отключения блокировки

    # Обработчики событий
    def on_close(self, event):
        """Обработчик закрытия программы"""
        if self.remaining_time > 0:
            # Запись времени в файл
            test_block.update_json("remaining_time", self.remaining_time - self.elapsed_time)
        else:
            test_block.update_json("remaining_time", 0)  # Удаляем значение времени если таймер не активен
            test_block.update_json("username_blocking", "")  # Удаляем значение с именем пользователя для блокировки
        self.Hide()
        self.Close(True)
        self.Destroy()

    def on_input_changed(self, event):
        """
        Обработчик события выбора пользователя из списка
        """
        # Получаем значения из полей ввода.
        self.username_blocking = self.input_username.GetValue()  # Получаем имя пользователя для блокировки
        test_block.update_json("username_blocking",
                               self.username_blocking
                               )  # Записываем имя пользователя для блокировки в файл
        combo_value = self.combo_box.GetValue()  # Получаем значение времени для блокировки из списка

        # Проверяем, что оба значения не пустые
        if self.input_username.GetValue() and int(combo_value) > 0:
            self.btn_ok.Enable()  # Активируем кнопку, если значения корректные
        else:
            self.btn_ok.Disable()  # Деактивируем кнопку, если значения некорректные или пустые

    def start_blocking(self, event):
        """
        Обработчик запуска задания блокировки. Кнопка ОК
        """
        username = self.input_username.GetValue()  # Получаем имя пользователя для блокировки

        # Настройка таймера
        hours = int(self.combo_box.GetValue())  # Получаем время для таймера
        self.remaining_time = int(hours * 60)  # Переводим в секунды
        self.elapsed_time = 0  # Инициализируем прошедшее время
        self.gauge.SetRange(self.remaining_time)  # Передаем время блокировки в статус строку
        self.gauge.SetValue(0)  # Начальное значение шкалы
        self.timer.Start(1000)  # Запуск таймера с интервалом 1 секунда
        self.btn_ok.Disable()  # Блокируем кнопку OK, пока таймер работает

        if username == test_block.username_session():
            dialog = wx.MessageDialog(self,
                                      _("Вы не можете назначить блокировку самому себе !!!\nВы являетесь АДМИНИСТРАТОРОМ системы.\nВыберите другого пользователя из списка."),
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
        test_block.update_json("username_blocking", self.username_blocking)

        if self.elapsed_time < self.remaining_time:
            self.elapsed_time += 1  # Увеличиваем прошедшее время
            self.gauge.SetValue(self.elapsed_time)  # Обновляем значение шкалы по мере увеличения времени
            # Сохраняем оставшееся время в файл при каждом тике таймера
            test_block.update_json("remaining_time", self.remaining_time - self.elapsed_time)
        else:
            self.timer.Stop()  # Останавливаем таймер, когда время истекло
            self.gauge.SetValue(0)  # Обнуляем статус строку
            test_block.update_json("remaining_time", 0)  # Удаляем значение времени, когда блокировка завершена.
            test_block.update_json("username_blocking", "")  # Удаляем значение с именем пользователя для блокировки
            # Логика блокировки учетной записи и рабочего стола.
            username = self.username_blocking  # Получаем имя пользователя для блокировки

            print(f"Имя пользователя - {username}")
            session_data = test_block.get_session_id_by_username(username)
            print("session_data", session_data)
            id_session_username = int(*(id for id in session_data if id.isdigit()))
            print(f"ID сесии - {id_session_username}")
            # Запускаем блокировку
            print("Запуск блокировки для пользователя")
            # TODO закомментировано для теста
            # test_block.blocking(username, id_session_username)
            self.btn_ok.Enable()  # Активируем кнопку

    def collapse_program(self, event):
        """
        Обработчик сворачивания программы в трей
        """
        self.Iconize(True)  # Свернуть окно в трей

    def disable_blocking(self, event):
        """
        Отключение блокировки
        """
        username = self.input_username.GetValue()  # Получаем имя пользователя для разблокировки

        if username != test_block.username_session() and username != "":
            self.timer.Stop()  # Остановка таймера
            self.gauge.SetValue(0)  # Стираем статус заполненности таймера

            test_block.unblock_user(username)
            dialog = wx.MessageDialog(self,
                                      _(f"Пользователь {username} разблокирован."),
                                      _("Предупреждение"),
                                      wx.ICON_WARNING
                                      )
            dialog.ShowModal()
            # Активируем кнопку OK
            self.btn_ok.Enable()
        elif username == "":
            dialog = wx.MessageDialog(self,
                                      _("Вы не указали пользователя для отключения блокировки."),
                                      _("Предупреждение"),
                                      wx.ICON_WARNING
                                      )
            dialog.ShowModal()
        elif username == test_block.username_session():
            dialog = wx.MessageDialog(self,
                                      _("Вы не можете заблокировать/разблокировать самого себя."),
                                      _("Предупреждение"),
                                      wx.ICON_WARNING
                                      )
            dialog.ShowModal()


# =============================================================================================================


def main():
    test_block.run_as_admin()
    app = wx.App(False)
    main_frame = Window(None)
    main_frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()
