import time

import wx
import wx.xrc
import gettext

import function
from app_wind_pass import WndPass

_ = gettext.gettext


###########################################################################
## Class Window
## Класс окна основного приложения
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
        # Основные переменные ==========================================
        self.timer = wx.Timer(self)  # Таймеp
        self.username_blocking = function.read_json("username_blocking")  # Имя пользователя для блокировки из файла
        self.remaining_time = function.read_json("remaining_time")  # Время задаваемой блокировки из файла
        self.elapsed_time = 0  #
        # ============================ END =============================
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.SetMinSize(wx.Size(600, 400))
        # Устанавливаем иконку для окна
        icon = wx.Icon('icon.ico', wx.BITMAP_TYPE_ICO)
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
        user_list = function.get_users()
        print(user_list)
        if not user_list:
            user_list = [_("Пользователи не найдены")]
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
        self.btn_disable_blocking.Disable()
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
        print(f"Время из файла - {self.remaining_time} - ({type(self.remaining_time)})")
        print(f"Имя из файла - {self.username_blocking} - ({type(self.username_blocking)})")

        # Если есть остаточное время и имя в файле данных data.json
        if self.remaining_time > 0 and len(self.username_blocking) >= 1:
            print(111)
            print("self.username_blocking", self.username_blocking)
            # Отключаем кнопку OK
            self.btn_ok.Disable()
            # Включаем кнопку отключения блокировки
            self.btn_disable_blocking.Enable()
            # Определяем какой пользователь был выбран при продолжении отсчета времени если был остаток в файле.
            self.input_username.SetValue(self.username_blocking)
            # Отключаем кнопку
            self.input_username.Disable()
            # Запускаем таймер
            self.elapsed_time = 0
            self.gauge.SetRange(self.remaining_time)
            self.gauge.SetValue(self.elapsed_time)
            self.timer.Start(1000)  # Запускаем таймер, если есть оставшееся время
        # Если время 0 а имя пользователя есть
        elif self.remaining_time == 0 and len(self.username_blocking) >= 1:
            print(222)
            self.remaining_time = 0
        # Если время есть, а имени нет
        elif self.remaining_time > 0 and len(self.username_blocking) == 0:
            print(333)
            # Очищаем имя пользователя для блокировки в файле
            function.update_json("username_blocking", "")
            # Очищаем время блокировки в файле
            function.update_json("remaining_time", 0)
        # END - логика если есть остаточное время в файле.
        # ------------------------------------------------

        # Подключаемые события в программе
        self.input_username.Bind(wx.EVT_TEXT, self.on_input_changed)
        self.input_time.Bind(wx.EVT_COMBOBOX, self.on_input_changed)
        self.input_time.Disable()

        self.Bind(wx.EVT_TIMER, self.run_on_timer, self.timer)  # Событие, при запуске таймера
        self.Bind(wx.EVT_CLOSE, self.on_close)  # Событие, закрытия окна
        self.btn_ok.Bind(wx.EVT_BUTTON, self.start_blocking)  # Событие, при нажатии кнопки OK (запуск задания)
        self.collapse_window.Bind(wx.EVT_BUTTON, self.collapse_program)  # Событие, свернуть окно
        self.btn_disable_blocking.Bind(wx.EVT_BUTTON, self.disable_blocking)  # Событие, отключения блокировки

    # Обработчики событий
    def on_close(self, event):
        """Обработчик закрытия программы"""
        print("on_close", self.remaining_time, type(self.remaining_time))
        # Если время больше ноля и имя пользователя не пустое
        if self.remaining_time > 0 and len(self.username_blocking) >= 1:
            # Запись времени в файл
            function.update_json("remaining_time", self.remaining_time - self.elapsed_time)
            print("1as")
        # Если время равно 0
        elif self.remaining_time == 0:
            # Удаляем значение времени если таймер не активен
            function.update_json("remaining_time", 0)
            # Удаляем значение с именем пользователя для блокировки
            function.update_json("username_blocking", "")
            print("2as")
        # Если время больше ноля, но имя пустое
        elif self.remaining_time > 0 and len(self.username_blocking) == 0:
            # Очищаем время если таймер не активен
            function.update_json("remaining_time", 0)
            # Сбрасываем поле с временем на 0
            self.input_time.SetSelection(0)

        self.Hide()
        self.Destroy()

    def on_input_changed(self, event):
        """
        Обработчик события выбора пользователя из списка или времени
        """
        print(103)
        # Получаем значения из полей ввода.
        self.username_blocking = self.input_username.GetValue()  # Получаем имя пользователя для блокировки
        # Записываем имя пользователя для блокировки в файл
        function.update_json("username_blocking", self.username_blocking)
        self.remaining_time = int(self.input_time.GetValue())
        print(104, self.input_time.GetValue(), type(self.input_time.GetValue()))
        # Записывает выбранное время для блокировки
        function.update_json("remaining_time", self.remaining_time)

        # Проверяем запущена ли сессия искомого пользователя
        if function.get_session_id_by_username(self.username_blocking) is None:
            # Отключаем поле выбора времени для блокировки
            self.input_time.Disable()
            # Выводим сообщение что-бы выбранный пользователь зашел в систему (сессию)
            dialog = wx.MessageDialog(self,
                                      _(f"Выбранный пользователь: {self.username_blocking} не вошел в свой аккаунт "
                                        f"Windows.\nРЕШЕНИЕ:\n"
                                        f"1 - Нужно зайти в его аккаунт.\n2 - Далее перейти в аккаунт АДМИНИСТРАТОРА\n"
                                        f"3 - И провести процедуру настройки блокировки снова."
                                        ),
                                      _("Предупреждение"),
                                      wx.ICON_WARNING
                                      )
            dialog.ShowModal()
            dialog.Destroy()
            # Сбрасываем выбор пользователя
            self.input_username.SetSelection(-1)
            self.btn_disable_blocking.Disable()
            function.update_json("username_blocking", "")
        else:
            self.input_time.Enable()
            self.btn_disable_blocking.Enable()

        combo_value = self.input_time.GetValue()  # Получаем значение времени для блокировки из списка

        # Проверяем, указаны ли время и пользователь и запущена ли сессия.
        session_id = function.get_session_id_by_username(self.username_blocking)  # Получаем данные о сессии
        if self.input_username.GetValue() and int(combo_value) > 0 and session_id is not None:
            self.btn_ok.Enable()  # Активируем кнопку OK, если значения корректные
            self.input_time.Enable()  # Активируем поле с временем для блокировки
        else:
            self.btn_ok.Disable()  # Деактивируем кнопку, если значения некорректные или пустые

    def start_blocking(self, event):
        """
        Обработчик запуска задания блокировки. Кнопка ОК
        """
        username = self.input_username.GetValue()  # Получаем имя пользователя для блокировки

        # Настройка таймера
        hours = int(self.input_time.GetValue())  # Получаем время для таймера
        self.remaining_time = int(hours * 60)  # Переводим в секунды
        self.elapsed_time = 0  # Инициализируем прошедшее время
        self.gauge.SetRange(self.remaining_time)  # Передаем время блокировки в статус строку
        self.gauge.SetValue(0)  # Начальное значение шкалы
        self.timer.Start(1000)  # Запуск таймера с интервалом 1 секунда
        self.btn_ok.Disable()  # Блокируем кнопку OK, пока таймер работает

        if username == function.username_session():
            dialog = wx.MessageDialog(self,
                                      _("Вы не можете назначить блокировку самому себе !!!\n"
                                        "Выберите другого пользователя из списка."
                                        ),
                                      _("Предупреждение"),
                                      wx.ICON_WARNING
                                      )
            dialog.ShowModal()
            dialog.Destroy()

            self.timer.Stop()  # Останавливаем таймер
            self.gauge.SetValue(0)  # Обнуляем статус строку
            # Очищаем поле с именем и временем
            self.input_username.SetSelection(-1)
            self.input_time.SetSelection(0)
            # Очищаем имя пользователя для блокировки в файле
            function.update_json("username_blocking", "")
            # Очищаем время блокировки в файле
            function.update_json("remaining_time", 0)

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

        else:
            self.timer.Stop()  # Останавливаем таймер, когда время истекло
            self.gauge.SetValue(0)  # Обнуляем статус строку
            # Удаляем значение времени в файле, когда блокировка завершена.
            function.update_json("remaining_time", 0)
            # Удаляем значение с именем пользователя для блокировки
            function.update_json("username_blocking", "")

            # =============== Логика блокировки учетной записи и рабочего стола.
            username = self.username_blocking  # Получаем имя пользователя для блокировки
            print(f"Имя пользователя - {username}")
            session_data = function.get_session_id_by_username(username)
            print("session_data", session_data)
            id_session_username = int(*(id for id in session_data if id.isdigit()))
            print(f"ID сесии - {id_session_username}")

            # TODO Запускаем блокировку ==========================
            print("Запуск блокировки для пользователя")
            function.blocking(username, id_session_username)
            # После того как отработала блокировка пользователя обнуляем поля ввода имя-время.
            # Стираем значение в поле имя пользователя.
            self.input_username.SetSelection(-1)
            # Стираем значение в поле выбора времени для блокировки
            self.input_time.SetSelection(0)
            # Активируем кнопку
            self.btn_ok.Enable()
            # todo ================= END ==============================

    def collapse_program(self, event):
        """
        Обработчик сворачивания программы в трей
        """
        self.Iconize(True)  # Свернуть окно в трей

    def disable_blocking(self, event):
        """
        Обработчик отключение блокировки
        """
        username = self.input_username.GetValue()  # Получаем имя пользователя для разблокировки

        # Если имя не совпадает с именем пользователя сессии и имя не пустое
        if username != function.username_session() and username != "":
            self.timer.Stop()  # Остановка таймера
            self.gauge.SetValue(0)  # Стираем статус заполненности таймера

            function.unblock_user(username)
            dialog = wx.MessageDialog(self,
                                      _(f"Пользователь {username} разблокирован."),
                                      _("Предупреждение"),
                                      wx.ICON_WARNING
                                      )
            dialog.ShowModal()
            # Активируем кнопку OK
            self.btn_ok.Enable()
            print(444)

            # Стираем значение в поле имя пользователя.
            self.input_username.SetSelection(-1)
            # Стираем значение в поле выбора времени для блокировки
            self.input_time.SetSelection(0)
            # Очищаем содержимое времени в файле
            function.update_json("remaining_time", 0)  # Записываем значение времени 0 в файл
            # Очищаем содержимое имени пользователя в файле
            function.update_json("username_blocking", "")  # Записываем пустую строку в файл

            # Активируем поле выбора пользователя
            self.input_username.Enable()
            # Отключаем поле выбора времени
            self.input_time.Disable()
            # Отключаем кнопку - "Отключить блокировку"
            self.btn_disable_blocking.Disable()
            print(555)
        # Если имя пользователя пустое
        elif username == "":
            dialog = wx.MessageDialog(self,
                                      _("Вы не указали пользователя для отключения блокировки."),
                                      _("Предупреждение"),
                                      wx.ICON_WARNING
                                      )
            dialog.ShowModal()
        # Если имя пользователя совпадает с именем пользователя сесии
        elif username == function.username_session():
            dialog = wx.MessageDialog(self,
                                      _("Вы не можете заблокировать/разблокировать самого себя."),
                                      _("Предупреждение"),
                                      wx.ICON_WARNING
                                      )
            dialog.ShowModal()

            self.btn_disable_blocking.Disable()  # Отключаем кнопку блокировки
            self.input_username.SetSelection(-1)  # Очищаем поле с именем пользователя
            self.input_time.SetSelection(0)  # Сброс поля времени блокировки
            # Очистка значений в файлах
            function.update_json("remaining_time", 0)  # Удаляем значение времени, когда блокировка завершена.
            function.update_json("username_blocking", "")  # Удаляем значение с именем пользователя для блокировки


# =============================================================================================================


def main():
    # Запускаем приложение как администратор
    function.run_as_admin()

    app = wx.App(False)
    main_frame = Window(None)
    # main_frame.Show()
    main_frame.Hide()


    # Выводим предупреждение перед запуском приложения
    wx.MessageBox("Программа должна быть запущена от имени АДМИНИСТРАТОРА\nИначе работа программы будет некорректной",
                  "Напоминание",
                  wx.OK | wx.ICON_AUTH_NEEDED)


    # Создаем и отображаем окно ввода пароля
    dlg = WndPass(None)
    dlg.ShowModal()

    if dlg.password_check:
        main_frame.Show()

    app.MainLoop()

if __name__ == "__main__":
    main()