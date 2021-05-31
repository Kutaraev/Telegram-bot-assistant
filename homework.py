import os
import time

import requests
import telegram
import logging
from dotenv import load_dotenv

load_dotenv()

PRAKTIKUM_TOKEN = os.getenv('PRAKTIKUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
YANDEX_API = 'https://praktikum.yandex.ru/api/user_api/homework_statuses/'


def parse_homework_status(homework):
    statuses = {'reviewing': 'Работа находится в проверке',
                'approved': ('Ревьюеру всё понравилось, '
                             'можно приступать к следующему уроку.'),
                'rejected': 'К сожалению в работе нашлись ошибки.'}

    '''Проверяем, что ключи homework_name и homework_status есть в словаре.
    А если их нет, то пишем это в лог. Не совсем понял, что значит
    "прислали чего то не то" в замечаниях. Зачем нужно проверять что-то нето,
    если нужны конкретные ключи?'''

    if 'homework_name' in homework or 'homework_status' in homework:
        homework_name = homework['homework_name']
        homework_status = homework['status']
    else:
        logging.error('Одного из нужных ключей нет ы словаре')
    if homework_status in statuses:
        return (f'У вас проверили работу '
                f'"{homework_name}"!\n\n{statuses[homework_status]}')
    else:
        logging.error('Статуса работы нет в списке.')


def get_homework_statuses(current_timestamp):
    headers = {'Authorization': f'OAuth {PRAKTIKUM_TOKEN}'}
    params = {'from_date': current_timestamp}
    try:
        homework_statuses = requests.get(
            YANDEX_API,
            params=params, headers=headers)
        return homework_statuses.json()
    except requests.exceptions.RequestException as e:
        logging.error(f'Бот столкнулся с ошибкой: {e}')
        return None


def send_message(message, bot_client):
    return bot_client.send_message(CHAT_ID, message)


def main():
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    logging.basicConfig(level=logging.DEBUG)
    logging.debug('TrickyAbbot запущен!')
    current_timestamp = int(time.time())

    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            if new_homework.get('homeworks'):
                send_message(parse_homework_status(
                    new_homework.get('homeworks')[0]), bot)
                logging.info('Сообщение отправлено!')
            current_timestamp = new_homework.get(
                'current_date', current_timestamp)
            time.sleep(300)
        except Exception as e:
            error_msg = f'Бот столкнулся с ошибкой: {e}'
            bot.send_message(CHAT_ID, error_msg)
            time.sleep(5)


if __name__ == '__main__':
    main()
