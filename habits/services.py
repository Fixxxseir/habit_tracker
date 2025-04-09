import requests
from requests import RequestException

from config import settings


def send_telegram_message(message, chat_id):
    """
    Функция реализует отправку сообщения в телеграм через запрос
    """
    params = {"text": message, "chat_id": chat_id}
    try:
        response = requests.get(
            f"{settings.TELEGRAM_URL}{settings.TELEGRAM_TOKEN}/sendMessage",
            params=params,
        )
        response.raise_for_status()
    except RequestException as e:
        print(f"Ошибка отправки: {e}")
