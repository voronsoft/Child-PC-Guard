"""Обработчики событий для файла app_admin.py"""
import os
import subprocess
import time

import wx

import config_localization
import function
from app_wind_bot import BotWindow
from app_wind_documentation import DocWindow
from app_wind_lang import LanguageWnd
from app_wind_pass import WndPass
from config_app import PATH_LOG_FILE, path_timer_exe, path_unblock_usr_exe

# Подключаем локализацию
_ = config_localization.setup_locale(function.read_data_json("language"))


# app_admin_event_handlers.py
class EventHandlers:
    """Класс обработчиков событий для основного приложения"""

    def __init__(self, main_window):
        self.main_window = main_window  # Сохраняем ссылку на основной класс

    # Обработчики событий --------------------------------

    def on_input_changed(self, event):
        """
        Обработчик события выбора имени пользователя и времени
        """
        # =============== Получаем значения из полей ввода ================
        # Имя пользователя получаем из поля выбора и записываем в файл данных
        username_choice = self.main_window.input_username.GetValue()  # Получаем имя пользователя для блокировки
        print("Произошло событие в поле выбора пользователя:", username_choice)
        # Записываем имя пользователя для блокировки в файл данных.
        function.update_data_json("username_blocking", username_choice)
        # Обновляем атрибут в классе
        self.main_window.username_blocking = function.read_data_json("username_blocking")

        # Время блокировки получаем из поля выбора и записываем в файл данных переведя в секунды
        # TODO Перевести значение в часы после разработки (*3600)
        time_choice = int(self.main_window.input_time.GetValue()) * 3600
        # Записывает выбранное время для блокировки в файл данных.
        function.update_data_json("remaining_time", time_choice)
        # Обновляем атрибут в классе
        self.main_window.remaining_time = function.read_data_json("remaining_time")

        # Получаем данные о сессии
        session_id = function.get_session_id_by_username(self.main_window.username_blocking)

        # ==========================================================================
        # Проверяем запущена ли сессия искомого пользователя если нет стираем данные
        if function.get_session_id_by_username(self.main_window.username_blocking) is None:
            self.main_window.input_time.Disable()  # Отключаем поле выбора времени для блокировки
            self.main_window.btn_disable_blocking.Disable()  # Отключаем кнопку - Отключить блокировку

            # Выводим сообщение что-бы выбранный пользователь зашел в систему (сессию)
            dialog = wx.MessageDialog(
                    None,
                    f"{_("Выбранный пользователь:")} {self.main_window.username_blocking} {_("не вошел в свой аккаунт Windows.\nРЕШЕНИЕ:\n1 - Нужно зайти в его аккаунт.\n2 - Запустить программу от имени АДМИНИСТРАТОРА\n3 - Провести процедуру настройки блокировки снова.")}",
                    _("Предупреждение"),
                    wx.ICON_WARNING,
            )
            dialog.ShowModal()
            dialog.Destroy()

            # Сбрасываем выбор пользователя
            self.main_window.input_username.SetSelection(-1)  # Сбрасываем поле имени
            function.update_data_json("username_blocking", "")  # Стираем имя пользователя в файле
            self.main_window.username_blocking = function.read_data_json(
                    "username_blocking"
            )  # Обновляем атрибут имени пользователя
            # Сбрасываем выбор времени
            self.main_window.input_time.SetSelection(0)  # Обнуляем время в поле
            function.update_data_json("remaining_time", 0)  # Стираем значение времени в файле
            self.main_window.remaining_time = function.update_data_json("remaining_time", 0)  # Обновляем атрибут времени блокировки
        else:
            self.main_window.input_time.Enable()  # Активируем поле выбора времени
            self.main_window.btn_disable_blocking.Enable()  # Активируем кнопку - Отключить блокировку

        # Проверяем, указаны ли пользователь и время и запущена ли сессия.
        if self.main_window.input_username.GetValue() and int(time_choice) > 0 and session_id is not None:
            self.main_window.btn_ok.Enable()  # Активируем кнопку OK, если значения корректные
            self.main_window.input_time.Enable()  # Активируем поле с временем для блокировки
        else:
            self.main_window.btn_ok.Disable()  # Деактивируем кнопку, если значения некорректные или пустые

    def start_blocking(self, event):
        """
        Обработчик запуска задания блокировки. Кнопка ОК
        """
        # function.send_bot_telegram_message(_("Запуск задания блокировки"))

        username = self.main_window.input_username.GetValue()  # Получаем имя пользователя для блокировки
        hours = int(self.main_window.input_time.GetValue())  # Получаем время для таймера из поля выбора времени
        self.main_window.remaining_time = int(hours * 3600)  # TODO Перевести значение в часы после разработки (*3600)

        # Настройка таймера
        self.main_window.elapsed_time = 0  # Инициализируем прошедшее время
        self.main_window.gauge.SetRange(self.main_window.remaining_time)  # Передаем время блокировки в статус строку
        self.main_window.gauge.SetValue(0)  # Начальное значение шкалы
        self.main_window.timer.Start(1000)  # Запуск таймера с интервалом 1 секунда
        self.main_window.btn_ok.Disable()  # Блокируем кнопку OK, пока таймер работает
        self.main_window.input_username.Disable()  # Блокируем поле имени пользователя
        self.main_window.input_time.Disable()  # Блокируем поле выбора времени блокировки

        if username == function.username_session():
            dialog = wx.MessageDialog(
                    None,
                    _(
                            "Внимание убедитесь что вы выбрали не АДМИНИСТРАТОРА !!!\nТолько АДМИНИСТРАТОР может снять блокировку !!!.\nВ противном случае блокировку уже не снять.\nРЕШЕНИЕ - ПЕРЕУСТАНОВКА WINDOWS !!!"
                    ),
                    _("Предупреждение"),
                    wx.ICON_WARNING,
            )
            dialog.ShowModal()
            dialog.Destroy()

    def run_on_timer(self, event):
        """
        Обработчик таймера.
        """
        # Сохраняем имя пользователя для блокировки в файл
        function.update_data_json("username_blocking", self.main_window.username_blocking)

        if self.main_window.elapsed_time < self.main_window.remaining_time:
            self.main_window.elapsed_time += 1  # Увеличиваем прошедшее время
            self.main_window.gauge.SetValue(self.main_window.elapsed_time)  # Обновляем значение шкалы по мере увеличения времени
            # Сохраняем оставшееся время в файл при каждом тике таймера
            function.update_data_json("remaining_time", self.main_window.remaining_time - self.main_window.elapsed_time)
            # Обновление значения текста в таймере главного окна (01:10:23)
            self.main_window.timer_time.SetLabel(function.seconds_to_hms(self.main_window.remaining_time - self.main_window.elapsed_time))

        else:
            self.main_window.timer.Stop()  # Останавливаем таймер, когда время истекло

            # =============== Логика блокировки учетной записи и рабочего стола.
            # TODO Запускаем блокировку ==========================
            username = self.main_window.username_blocking  # Получаем имя пользователя для блокировки
            session_data = function.get_session_id_by_username(username)  # Данные о сессии
            id_session_username = int(*(id for id in session_data if id.isdigit()))  # ID сессии
            function.blocking(username, id_session_username)  # Запуск
            # ====================== END ==========================

            # После того как отработала блокировка пользователя настраиваем интерфейс и обновляем данные.
            self.main_window.gauge.SetValue(0)  # Обнуляем статус строку

            function.update_data_json("remaining_time", 0)  # Удаляем значение времени в файле.
            function.update_data_json("username_blocking", "")  # Удаляем значение имени пользователя в файле.

            self.main_window.input_username.SetSelection(-1)  # Стираем значение в поле имя пользователя.
            self.main_window.input_username.Enable()  # Активируем поле выбора имени
            self.main_window.input_time.SetSelection(0)  # Стираем значение в поле выбора времени для блокировки
            self.main_window.input_time.Disable()  # Отключаем поле выбора времени
            self.main_window.timer_time.SetLabel("00:00:00")  # Обновляем время в поле таймера
            self.main_window.btn_disable_blocking.Disable()  # Отключаем кнопку отл=ключения блокировки

    def disable_blocking(self, event):
        """
        Обработчик отключение блокировки
        """
        username = self.main_window.username_blocking
        print("def disable_blocking:", username)

        # Отмена блокировки если имя пользователя пустое
        if username == "":
            dialog = wx.MessageDialog(
                    None, _("Вы не указали пользователя для отключения блокировки."), _("Предупреждение"), wx.ICON_WARNING
            )
            dialog.ShowModal()
        else:
            self.main_window.timer.Stop()  # Останавливаем таймер
            function.send_bot_telegram_message(
                    _("Блокировка для пользователя отключена: {usermane}").format(usermane=username)
            )
            self.main_window.gauge.SetValue(0)  # Стираем статус заполненности таймера

            # Стираем значение в поле имя пользователя.
            self.main_window.input_username.SetSelection(-1)
            # Очищаем значение имени пользователя в файле
            function.update_data_json("username_blocking", "")  # Удаляем значение с именем пользователя для блокировки.

            # Стираем значение в поле выбора времени для блокировки
            self.main_window.input_time.SetSelection(0)
            # Очищаем значение времени в файле
            function.update_data_json("remaining_time", 0)  # Удаляем значение времени в файле.
            # Стираем значение атрибута времени для блокировки в классе
            self.main_window.remaining_time = function.read_data_json("remaining_time")

            # Сбрасываем значение времени в поле - "Осталось времени до блокировки:"
            self.main_window.timer_time.SetLabel("00:00:00")
            # Отключаем кнопку - Отключить блокировку
            self.main_window.btn_disable_blocking.Disable()
            self.enable_fields()

            # Сообщение
            dialog = wx.MessageDialog(
                    None,
                    f"{_("(1)Пользователь")} - {username} - {_("разблокирован")}",
                    _("Предупреждение"),
                    wx.ICON_WARNING,
            )
            dialog.ShowModal()

    def disable_fields(self):
        """Функция отключения полей для ввода"""
        # Деактивируем все поля главного приложения
        self.main_window.input_username.Disable()  # Поле имени пользователя для блокировки
        self.main_window.input_time.Disable()  # Поле времени
        self.main_window.gauge.Disable()  # Поле прогресса времени
        self.main_window.btn_disable_blocking.Disable()  # Кнопка - Отключить блокировку
        self.main_window.btn_ok.Disable()  # Кнопка ОК
        # Деактивируем кнопки в тулбаре
        self.main_window.tool_bar.EnableTool(self.main_window.btn_tool_log.GetId(), False)
        self.main_window.tool_bar.EnableTool(self.main_window.btn_tool_timer.GetId(), False)
        # self.main_window.tool_bar.EnableTool(self.main_window.btn_tool_monitor.GetId(), False)
        self.main_window.tool_bar.EnableTool(self.main_window.btn_tool_clear_data.GetId(), False)
        self.main_window.tool_bar.EnableTool(self.main_window.btn_tool_run_unblock_usr.GetId(), False)
        # self.main_window.tool_bar.EnableTool(self.main_window.btn_tool_info.GetId(), True)
        self.main_window.tool_bar.EnableTool(self.main_window.btn_tool_bot.GetId(), False)

        self.main_window.tool_bar.EnableTool(self.main_window.btn_tool_unblock_interface.GetId(), False)
        self.main_window.tool_bar.EnableTool(self.main_window.btn_tool_block_interface.GetId(), False)

    def enable_fields(self):
        """Функция включения (активации) полей для ввода"""
        # Активируем поля если пароль совпал.
        self.main_window.input_username.Enable()  # Поле имени пользователя для блокировки
        self.main_window.gauge.Enable()  # Поле прогресса времени
        # Активируем кнопки в тулбаре
        self.main_window.tool_bar.EnableTool(self.main_window.btn_tool_log.GetId(), True)
        self.main_window.tool_bar.EnableTool(self.main_window.btn_tool_timer.GetId(), True)
        # self.main_window.tool_bar.EnableTool(self.main_window.btn_tool_monitor.GetId(), True)
        self.main_window.tool_bar.EnableTool(self.main_window.btn_tool_clear_data.GetId(), True)
        self.main_window.tool_bar.EnableTool(self.main_window.btn_tool_run_unblock_usr.GetId(), True)
        # self.main_window.tool_bar.EnableTool(self.main_window.btn_tool_info.GetId(), True)
        self.main_window.tool_bar.EnableTool(self.main_window.btn_tool_bot.GetId(), True)
        self.main_window.tool_bar.EnableTool(self.main_window.btn_tool_unblock_interface.GetId(), True)
        self.main_window.tool_bar.EnableTool(self.main_window.btn_tool_block_interface.GetId(), True)
        # self.main_window.tool_bar.EnableTool(True)

    def enable_fields_tool_bar(self):
        """
        Функция включения (активации) полей для ввода.
        Если было ОСТАТОЧНОЕ время в файле с данными.
        """
        self.main_window.tool_bar.EnableTool(self.main_window.btn_tool_unblock_interface.GetId(), True)
        self.main_window.tool_bar.ToggleTool(self.main_window.btn_tool_block_interface.GetId(), True)

    # Обработчики тулбара --------------------------------
    def on_lang(self, event):
        """Запуск окна выбора языков"""
        lang_app = LanguageWnd(None)
        lang_app.ShowModal()

    def on_run_log(self, event):
        """Запуск просмотра логов программы"""
        try:
            os.startfile(PATH_LOG_FILE)  # Открываем файл в ассоциированном приложении (обычно Блокнот)
        except Exception as e:
            function.show_message_with_auto_close(f"{_("Не удалось открыть файл:")} {str(e)}", {_("Ошибка")})

    def on_run_timer(self, event):
        """Запуск окна таймера"""
        try:
            # Запускаем .exe файл через subprocess
            subprocess.Popen([path_timer_exe])
        except Exception as e:
            # Выводим сообщение об ошибке, если не удалось запустить приложение
            function.show_message_with_auto_close(f"{path_timer_exe}\n{str(e)}", _("Ошибка"))
            # Записываем лог
            self.log_error(f"{path_timer_exe}\n{str(e)}")

    def on_run_unblock(self, event):
        """Запуск программы для разблокировки пользователя"""
        try:
            # Запускаем .exe файл через subprocess
            subprocess.Popen([path_unblock_usr_exe])
        except Exception as e:
            # Выводим сообщение об ошибке, если не удалось запустить приложение
            function.show_message_with_auto_close(f"{path_unblock_usr_exe}\n{str(e)}", _("Ошибка"))
            # Записываем лог
            self.log_error(f"{path_unblock_usr_exe}\n{str(e)}")

    def on_run_clear_data(self, event):
        """
        Очистка данных в полях и файле с данными.
        Полный сброс задания блокировщика.
        PS.
        НЕ СНИМАЕТ БЛОКИРОВКУ С ПОЛЬЗОВАТЕЛЯ
        """
        # Останавливаем таймер (если он работает)
        self.main_window.timer.Stop()
        # Сбрасываем статус строку таймера (прошедшее время)
        self.main_window.gauge.SetValue(0)  # Начальное значение шкалы
        # Стираем значение в поле имя пользователя.
        self.main_window.input_username.SetSelection(-1)
        # Стираем значение в поле выбора времени для блокировки
        self.main_window.input_time.SetSelection(0)
        # Сбрасываем значение времени в поле - "Осталось времени до блокировки:"
        self.main_window.timer_time.SetLabel("00:00:00")
        # Очищаем содержимое времени в файле
        function.update_data_json("remaining_time", 0)  # Записываем значение времени 0 в файл
        # Очищаем содержимое имени пользователя в файле
        function.update_data_json("username_blocking", "")  # Записываем пустую строку в файл
        function.send_bot_telegram_message(_("Настройки программы сброшены через кнопку в интерфейсе"))

        # Активируем поле выбора имени пользователя для блокировки
        self.main_window.input_username.Enable()
        # Отключаем поле выбора времени блокировки
        self.main_window.input_time.Disable()
        # Отключаем кнопку - Отключить блокировку
        self.main_window.btn_disable_blocking.Disable()
        # Отключаем кнопку ОК
        self.main_window.btn_ok.Disable()

        # Вывод сообщения об успешной очистке
        function.show_message_with_auto_close(_("Настройки программы сброшены!"), _("СБРОС ДАННЫХ"))

    def on_run_info(self, event):
        """Запуск окна справки"""
        doc_app = DocWindow(None)
        doc_app.Show()

    def on_run_bot(self, event):
        """Запуск окна настройки для оповещения для telegram"""
        doc_app = BotWindow(None)
        doc_app.Show()

    def on_block_interface(self, event):
        """Блокировка интерфейса при нажатии кнопки - Заблокировать интерфейс"""
        # Блокируем все поля окна
        self.disable_fields()
        # Но оставляем одну кнопку активной - "Разблокировать интерфейс"
        self.main_window.tool_bar.EnableTool(self.main_window.btn_tool_unblock_interface.GetId(), True)

    def on_unblock_interface(self, event):
        """Разблокировка интерфейса при попытке нажать в тулбаре на кнопку - Разблокировать интерфейс"""
        # Отображаем окно ввода пароля
        dlg = WndPass(None)
        dlg.ShowModal()

        # Если пароль не совпал
        if not dlg.password_check:
            self.main_window.Close()
            self.enable_fields_tool_bar()
            print("1 Должен активироваться интерфейс")
            function.send_bot_telegram_message(
                    _("Кто то пытается разблокировать интерфейс программы\nПароль не совпал")
            )
        # Если пароль совпал и есть остаточное время в БД
        elif dlg.password_check and function.read_data_json("remaining_time"):
            self.enable_fields()
            self.main_window.input_username.Enable(False)
            self.main_window.btn_disable_blocking.Enable(True)
            function.send_bot_telegram_message(_("Интерфейс программы разблокирован"))
            print("2 Должен активироваться интерфейс")
        # Если пароль совпал
        elif dlg.password_check:
            self.enable_fields()
            function.send_bot_telegram_message(_("Интерфейс программы разблокирован"))
            print("3 Должен активироваться интерфейс")

    def log_error(self, message):
        """Логирование ошибок в файл."""
        try:
            with open(PATH_LOG_FILE, "a", encoding="utf-8") as log_file:
                log_file.write(f"CPG({time.strftime('%Y-%m-%d %H:%M:%S')}) - " f"{message}\n==================\n")
        except Exception as e:
            print(f"(1)Ошибка при записи лога в файл: {str(e)}")
            function.show_message_with_auto_close(f"{_("Ошибка при записи в файл лога:\n")}{str(e)}", _("ОШИБКА"))

    # =============================================================================================================
