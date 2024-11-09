--------------------------------------------------------------------------------------
- Команды компиляции приложений
pyinstaller app_admin.spec             Основное приложение.
pyinstaller app_lock_unlock_usr.spec   Снятие блокировки с пользователя.
pyinstaller app_monitor.spec           Мониторинг работы "Основного приложения"
pyinstaller app_tg_bot.spec            Бот telegram
pyinstaller app_timer.spec             Таймер времени до начала блокировки.
pyinstaller app_uninstaller.spec       Деинсталлятор приложения

--------------------------------------------------------------------------------------



--------------------------------------------------------------------------------------
Обновление файла с зависимостями:
--> pip freeze > requirements.txt
Установка модулей из файла с зависимостями
--> pip install -r requirements.txt
--------------------------------------------------------------------------------------



--------------------------------------------------------------------------------------
Команда для gettext создание .pot файла всего приложения
В команде перечислены файлы в которых будет проходить поиск функции перевода _()
xgettext -o locale/messages.pot -L Python app_admin.py app_lock_unlock_usr.py app_timer.py app_wind_bot.py app_wind_documentation.py app_wind_exit_prog.py app_wnd_input_first_pass.py app_wind_lang.py app_wind_pass.py app_wind_tray_icon.py app_tg_bot.py function.py

1 Команда для создания .po файла для русского языка
msginit --input=locale/messages.pot --output-file=locale/ru/LC_MESSAGES/messages.po --locale=ru_RU

2 Команда для создания .po файла для английского языка
msginit --input=locale/messages.pot --output-file=locale/en/LC_MESSAGES/messages.po --locale=en_US

3 Команда для создания .po файла для украинского языка
msginit --input=locale/messages.pot --output-file=locale/uk/LC_MESSAGES/messages.po --locale=uk_UA

--------------------------------------------------------------------------------------



--------------------------------------------------------------------------------------
Тестовый адрес (нужно указать свой chat_id) "chat_id": 631191214,
--------------------------------------------------------------------------------------
