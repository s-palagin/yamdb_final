![workflow](https://github.com/s-palagin/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)


### yamdb_final

  
<font size = 3>
Проект **YaMDb** является сервисом, который собирает отзывы пользователей на произведения. 
Произведения делятся на категории, например «Книги», «Фильмы» и «Музыка». Список категорий может быть расширен администратором.
Произведениям может быть присвоен жанр из списка, который определяет администратор.

<font size = 3>Пользователи могут оставлять текстовые отзывы к произведениям и ставить произведению оценку в диапазоне от одного до десяти — из пользовательских оценок формируется усреднённая оценка произведения — рейтинг.
В сервисе реализована ролевая модель — существуют как обычные пользователи, так и модераторы и администраторы.
Модераторы имеют право удалять и редактировать любые отзывы и комментарии, администраторы имеют максимальные права на изменение данных сервиса.

<font size = 3>Сервис реализован с помощью фреймворков **Django**, **Django Rest Framework** и предоставляет REST API для доступа к своему функционалу
Проект развернут в **Docker -контейнере** с использованием веб-серверов **_Gunicorn_**, **_Nginx_** и настроен для работы с базой данных **PostgreSQL**

  ### Как запустить проект:

<font size = 3>Клонировать репозиторий:  ```git clone https://github.com/s-palagin/yamdb_final.git```
Перейти в папкуcd yamdb_final/infra:
```
cd yamdb_final/infra
```

<font size = 3>В текущей папке создать файл .env по следующему шаблону:
```
# Django SECRET_KEY
SECRET_KEY=p&l%385148kslhtyn^##a1)ilz@4zqj=rq&agdol^##zgl9(vs
# имя базы данных
DB_NAME=postgres
# логин для подключения к базе данных
POSTGRES_USER=postgres
# пароль для подключения к БД
POSTGRES_PASSWORD=postgres
# название сервиса (контейнера)
DB_HOST=db
# порт для подключения к БД
DB_PORT=5432
```
<font size = 3>Выполнить сборку контейнеров:
```
docker-compose up -d --build
```
Выполнить миграции: 
```
docker-compose exec web python manage.py migrate
```
Запустите команду управления коллекцией статических файлов:
```
docker-compose exec web python manage.py collectstatic --noinput
```
Для создания суперпользователя используйте команду:
```
docker-compose exec web python manage.py createsuperuser
```

  ### Описание REST API:

<font size = 3> Пример запроса получения списка произведений:
```
http://localhost/api/v1/titles/
```
Ответ сервера:
``` 
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "name": "string",
        "year": 0,
        "rating": 0,
        "description": "string",
        "genre": [
          {
            "name": "string",
            "slug": "string"
          }
        ],
        "category": {
          "name": "string",
          "slug": "string"
        }
      }
    ]
  }
]
```
Получение отзывов на произведение:
```
http://localhost//api/v1/titles/{title_id}/reviews/
```
Ответ сервера:
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "text": "string",
        "author": "string",
        "score": 1,
        "pub_date": "2019-08-24T14:15:22Z"
      }
    ]
  }
]
```

Для получения подробного описания REST API, предоставляемого сервисом, необходимо перейти на

  
http://localhost/redoc/