import os
import gettext

# Получаем путь к каталогу с переводами (locale)
LOCALE_PATH = os.path.join(os.path.dirname(__file__), 'locale')


# Функция для настройки локализации
def setup_locale(lang='en'):
    """
    Устанавливает язык для приложения.

    :param lang: Код языка, например, 'ru', 'en', 'uk'
    """

    # Загружаем перевод для указанного языка
    translation = gettext.translation('messages',  # Указываем домен
                                      LOCALE_PATH,  # Передаем путь к папке с локализацией относительно данного файла
                                      languages=[lang],  # Указываем язык локализации
                                      fallback=True  # Если перевод для указанного языка отсутствует,
                                      # будет использоваться исходный текст используемый в коде
                                      )

    # Устанавливаем функцию перевода как глобальную
    translation.install()

    # Возвращаем функцию gettext для дальнейшего использования
    return translation.gettext

if __name__ == '__main__':
    print("LOCALE_PATH ", LOCALE_PATH)
