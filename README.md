![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)

# Telegram Bot-assistant
Бот-ассистент для проверки статуса домашней работы.

## Описание
Проект представляет собой Телеграм-бота, который выполняет следующие функции:
1. Обращается к API сервиса Практикум.Домашка.
2. Узнает, взята ли домашняя работа в ревью и ее статус (проверяется/принята/есть замечания)
3. Отправляет результат в Телеграм-чат.

## Технологии
- [Python 3](https://www.python.org/downloads/)
- [Python Telegram Bot](https://python-telegram-bot.readthedocs.io/en/stable/)
- [Git](https://github.com/)
- [Visual Studio Code](https://code.visualstudio.com/Download)

## Установка
1. Клонировать репозиторий
```
git clone https://github.com/Kutaraev/Telegram-bot-assistant.git
```
2. Создать виртуальное окружение
```
python -m venv venv
```
3. Активировать виртуальное окружение
```
source venv/scripts/activate
```
4. Установить необходимые пакеты для работы приложения из файла зависимостей
```
pip install -r requirements.txt
```

## Функционал
В этом разделе описаны основные функции, используемые в программе, и логика их работы.
1.  В функции `main()` прописаны основные этапы выполнения программы. Последовательность выполняемых действий следующая:
- Сделать запрос к API;
- Проверить ответ;
- Если есть обновление — получить статус домашней работы и отправить сообщение в Telegram;
- Подождать некоторое время и сделать новый запрос.
2. Функция `get_homework_statuses(current_timestamp)` делает запрос к эндпоинту API-сервиса. В качестве параметра функция получает временную метку `current_timestamp`. Если ответ успешен - функция преобразовывает ответ API из формата JSON в тип данных Python.
3. Функция `parse_homework_status(homework)` извлекает из конкретной домашней работы `homework` статус этой домашней работы. В случае успеха, функция возвращает подготовленную для Telegram строку, содержащую один из статусов (в проверке/зачтено/отклонено).
4. Функция `send_message(message, bot_client)` отправляет сообщение в Telegram чат. Принимает на вход два параметра: строку с сообщением `message` и экземпляр бота `bot_client`.

## Дополнительная информация
Для обеспечения беспрерывной работы бота-ассистента можно разместить на облачном сервисе, например , [Heroku](https://www.heroku.com/).

## Контакты
Артем Кутараев – [@artem_kutaraev](https://t.me/artem_kutaraev) – artem.kutaraev@gmail.com  
Ссылка на проект – [https://github.com/Kutaraev/Telegram-bot-assistant.git](https://github.com/Kutaraev/Telegram-bot-assistant.git)  
