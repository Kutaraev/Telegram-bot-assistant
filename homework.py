import os
import time

import requests
import telegram
import logging
from dotenv import load_dotenv

load_dotenv()

PRAKTIKUM_TOKEN = os.getenv("PRAKTIKUM_TOKEN")
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


def parse_homework_status(homework):
    homework_name = homework['homework_name']
    homework_status = homework['status']
    if homework_status == 'rejected':
        verdict = 'К сожалению в работе нашлись ошибки.'
    else:
        verdict = ('Ревьюеру всё понравилось, '
                   'можно приступать к следующему уроку.')
    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


def get_homework_statuses(current_timestamp):
    headers = {'Authorization': f'OAuth {PRAKTIKUM_TOKEN}'}
    params = {'from_date': current_timestamp}
    homework_statuses = requests.get(
        'https://praktikum.yandex.ru/api/user_api/homework_statuses/',
        params=params, headers=headers)
    return homework_statuses.json()


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
            bot.polling(none_stop=True)
        except Exception as e:
            error_msg = f'Бот столкнулся с ошибкой: {e}'
            print(error_msg)
            bot.send_message(CHAT_ID, error_msg)
            time.sleep(5)


if __name__ == '__main__':
    main()
