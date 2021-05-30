import os
import time

import requests
import telegram
from dotenv import load_dotenv

load_dotenv()


PRAKTIKUM_TOKEN = os.getenv("PRAKTIKUM_TOKEN")
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

current_timestamp = int(time.time())


def get_homework_statuses(current_timestamp):
    headers = {'Authorization': f'OAuth {PRAKTIKUM_TOKEN}'}
    params = {'from_date': 0}
    homework_statuses = requests.get(
        'https://praktikum.yandex.ru/api/user_api/homework_statuses/',
        params=params, headers=headers)
    return homework_statuses.json()


new_homework = get_homework_statuses(current_timestamp)


def parse_homework_status(homework):
    homework_name = homework.get('homeworks')[0]['homework_name']
    homework_status = homework.get('homeworks')[0]['status']
    if homework_status == 'rejected':
        verdict = 'К сожалению в работе нашлись ошибки.'
    else:
        verdict = 'Ревьюеру всё понравилось, можно приступать к следующему уроку.'
    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'



bot = telegram.Bot(token=TELEGRAM_TOKEN)


def send_message(message, bot_client):
    return bot_client.send_message(CHAT_ID, message)


send_message(parse_homework_status(new_homework), bot)