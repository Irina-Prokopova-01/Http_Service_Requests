# API для сокращения URL

Этот проект представляет собой API 
для сокращения URL, 
реализованный с использованием Django и 
Django REST Framework. Он включает в 
себя функциональность для создания коротких 
URL и получения оригинальных URL по коротким 
идентификаторам. Кроме того, он предоставляет 
возможность асинхронного запроса данных с 
указанного URL.

## Установка

### Требования

• Python 3.8 или выше

• Django

• Django REST Framework

• aiohttp

### Установка зависимостей

1. Клонируйте репозиторий:

https://github.com/Irina-Prokopova-01/Http_Service_Requests

2. Установите необходимые пакеты:
 
   для pip: pip install -r requirements.txt
   для poetry: poetry install
   

3. Выполните миграции базы данных:
 
   python manage.py migrate

4. Запустите сервер:
 
   python manage.py runserver
   
## Использование API

### Создание короткого URL

POST /shorturl/urls/

Тело запроса:

{
    "original_url": "https://example.com"
}

Ответ:

{
    "short_id": "abc123"
}

Статусы:

• 201 Created — если короткий URL успешно создан.

• 400 Bad Request — если оригинальный URL не предоставлен.

### Получение оригинального URL

GET /shorturl/urls/{short_id}/

Параметры:

• short_id — короткий идентификатор, который вы получили при создании короткого URL.

Ответ:
При успешном запросе произойдет перенаправление на оригинальный URL.

Статусы:

• 307 Temporary Redirect — если оригинальный URL найден.

• 404 Not Found — если короткий URL не найден.

▎Асинхронный запрос данных с URL

POST /shorturl/fetch-data/

Тело запроса:

{
    "url": "https://example.com"
}


Ответ:
Возвращает содержимое указанного URL.

Статусы:

• 200 OK — если запрос успешен.

• 400 Bad Request — если URL не предоставлен.

• 500 Internal Server Error — если произошла ошибка при выполнении запроса.

## Лицензия

Для вопросов и предложений обращайтесь 
по адресу: [irina-ptokopova.style@yandex.ru].