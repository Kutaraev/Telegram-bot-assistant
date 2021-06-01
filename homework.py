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

    homework_name = homework.get('homework_name')
    homework_status = homework.get('status')
    if homework_name is None:
        logging.error('Работы нет в проверке')
        return 'Работы нет в проверке'
    if homework_status in statuses:
        return (f'У вас проверили работу '
                f'"{homework_name}"!\n\n{statuses[homework_status]}')
    else:
        logging.error('Статуса работы нет в списке.')
        return ('Полученный статус работы не совпадает'
                'ни с одним из известных статусов.')


def get_homework_statuses(current_timestamp):
    headers = {'Authorization': f'OAuth {PRAKTIKUM_TOKEN}'}
    params = {'from_date': current_timestamp}
    try:
        homework_statuses = requests.get(
            YANDEX_API,
            params=params, headers=headers)
    except requests.exceptions.RequestException as e:
        logging.error(f'Бот столкнулся с ошибкой: {e}')
    return homework_statuses.json()


def send_message(message, bot_client):
    return bot_client.send_message(CHAT_ID, message)


def main():
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    logging.basicConfig(level=logging.DEBUG)
    logging.debug('TrickyAbbot запущен!!')
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
