import wx
import os
import sys
import builtins
import function
from config_app import FOLDER_DATA

# -------------- Константы настройки домен и языки----------------------
# Языковой домен (название файла mo)
LANGDOMAIN = "I18Nwxapp"
# Список языков для поддержки в приложении ( для которых есть файлы перевода)
SUPPORTED_LANGUAGE = {"en": wx.LANGUAGE_ENGLISH,
                      "fr": wx.LANGUAGE_FRENCH,
                      "de": wx.LANGUAGE_GERMAN,
                      "r": wx.LANGUAGE_RUSSIAN,
                      }


# LANGDOMAIN = "messages"
# SUPPORTED_LANGUAGE = {
#         "en": wx.LANGUAGE_ENGLISH,
#         "uk": wx.LANGUAGE_UKRAINIAN,
#         "r": wx.LANGUAGE_RUSSIAN,
# }
# --------------------------- END --------------------------------------

# Устанавливаем пользовательский displayhook, чтобы предотвратить
# автоматическое использование глобальной переменной "_" (подчеркивание)
# для хранения значения последнего выражения, оцененного интерпретатором Python.
# Если этого не сделать, привязка _ к функции перевода gettext может быть перезаписана.
# Это особенно важно при отладке с помощью интерактивной оболочки (например, PyShell).

def _displayHook(obj):
    if obj is not None:
        print(repr(obj))


# Добавляем макрос перевода в builtins (встроенные функции), аналогично тому, как это делает gettext
builtins.__dict__['_'] = wx.GetTranslation

from wx.lib.mixins.inspection import InspectionMixin


# Класс приложения, которое наследуется от wx.App и включает InspectionMixin.
# InspectionMixin позволяет запускать интерактивный инспектор объектов wxPython.
class BaseApp(wx.App, InspectionMixin):
    def OnInit(self):
        # Инициализация инспектора объектов
        self.Init()  # Метод от InspectionMixin
        # Устанавливаем кастомный displayhook для предотвращения проблем с "_"
        sys.displayhook = _displayHook

        # Указываем путь к файлу где хранится информация о текущем языке интерфейса.
        self.appConfig = os.path.join(FOLDER_DATA, "data.json")

        # Создаем переменную для локали (изначально пустая).
        self.locale = None

        # Добавляем путь, где находятся файлы с переводами (.mo файлы).
        # Обычно это папка "locale" в корне проекта.
        wx.Locale.AddCatalogLookupPathPrefix('locale')

        # Вызываем метод для обновления языка интерфейса на выбранный.
        # Читаем значение языка из файла data.json через функцию.
        self.updateLanguage(function.read_data_json("language"))

        return True  # Успешная инициализация приложения

    def updateLanguage(self, lang):
        """
        Обновление языка интерфейса на выбранный пользователем.

        Важно удалить существующую локаль перед созданием новой,
        так как объект C++ может не быть удален вовремя, что может привести к сбоям.
        Если просто назначить новую локаль старой переменной,
        предыдущий объект не будет корректно уничтожен.

        :param string `lang`: код языка (например, "r", "en", "uk")
        """
        # Если запрашиваемый язык поддерживается, выбираем его,
        # иначе по умолчанию используем русский язык.
        if lang in SUPPORTED_LANGUAGE:
            selLang = SUPPORTED_LANGUAGE[lang]
        else:
            selLang = wx.LANGUAGE_RUSSIAN

        # Если локаль уже существует, удаляем ее перед созданием новой.
        if self.locale:
            assert sys.getrefcount(self.locale) <= 2  # Убеждаемся, что объект можно удалить
            del self.locale

        # Создаем объект локали для выбранного языка.
        self.locale = wx.Locale(selLang)

        # Если локаль создана успешно, загружаем соответствующий каталог переводов.
        if self.locale.IsOk():
            self.locale.AddCatalog(LANGDOMAIN)
        else:
            # Если локаль не поддерживается или не удалось загрузить, сбрасываем локаль.
            self.locale = None
