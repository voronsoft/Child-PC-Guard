import requests

from app_tg_bot import TOKEN
from function import read_data_json


def send_message_to_telegram_bot(token, chat_id, message):
    """
    Отправляет сообщение в Telegram-бота.

    :param token: Строка, токен вашего бота Telegram.
    :param chat_id: Строка или целое число, идентификатор чата, куда будет отправлено сообщение.
    :param message: Строка, сообщение, которое нужно отправить.
    """
    # Формируем URL для API Telegram
    url = f'https://api.telegram.org/bot{token}/sendMessage'

    # Определяем параметры запроса
    params = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'Markdown'  # Можно указать режим разметки, например, Markdown или HTML
    }

    # Отправляем запрос и получаем ответ
    response = requests.post(url, data=params)

    # Проверяем статус ответа
    if response.status_code == 200:
        print("Сообщение успешно отправлено!")
    else:
        print(f"Ошибка при отправке сообщения: {response.status_code} - {response.text}")

def main():
    bot_token = TOKEN  # Замените на токен вашего бота
    chat_id = read_data_json("id_tg_bot_parent")  # Замените на идентификатор чата
    message = 'Привет, это тестовое сообщение из второго приложения!'
    print("bot_token: ", bot_token)
    print("chat_id: ", chat_id)
    print("message: ", message)

    send_message_to_telegram_bot(bot_token, chat_id, message)

def get_id_chat(token):
    url = f'https://api.telegram.org/bot{token}/getUpdates'
    print(url)
    response = requests.get(url)
    print(response.json())

# Пример использования функции
if __name__ == "__main__":
    get_id_chat(TOKEN)
    main()



