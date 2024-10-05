import requests
from function import read_data_json

TOKEN = read_data_json("bot_token_telegram")

chat_id = read_data_json("id_tg_bot_parent")
URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'


def start_blocking_timer(duration):
    # Эмулируем начало отсчета времени
    print(f"Начинается отсчет времени блокировки на {duration} минут.")

    # Здесь вы можете добавить логику отсчета времени (например, time.sleep(duration * 60))

    # Отправка уведомления родителю о начале блокировки
    message = f"🔒 Тестовое сообщение родителю из приложения для теста."
    payload = {
            'chat_id': chat_id,
            'text': message
    }

    # Отправка POST-запроса к боту
    response = requests.post(URL, data=payload)

    if response.status_code == 200:
        print("Сообщение успешно отправлено!")
    else:
        print("Ошибка при отправке сообщения:", response.text)


if __name__ == "__main__":
    # Задайте продолжительность блокировки в минутах
    duration = 10  # например, 10 минут
    start_blocking_timer(duration)
