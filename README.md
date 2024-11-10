
#  Foodgram FastApi

Foodgram - Сервис для публикации рецептов, цель проекта объединить все самые интересные рецепты в одном удобном для всех месте под названием Fodgram! Авторизованный автор может публиковать рецепты, добавлять в избранное, подписываться на другого автора, скачивать список покупок.
В ходе написания проекта я смог углубленно изучить фреймворк FastAPI, библиотеку SQLAlchemy и работу с Docker.
Фронтенд-часть была взята из моего дипломного проекта foodgram-react и была частично изменена для корректной работы с FastAPI.
## Установка

Install my-project with npm

```bash
  git clone https://github.com/stas-zatushevskii/FoodGramFastAPI
  cd FoodGramFastAPI
```
    
## .env файл

Чтобы запустить этот проект, вам нужно будет добавить следующие переменные среды в ваш .env-файл.

`APP_TITLE` = "Продуктовый помощник"

`DATABASE_URL` = "postgresql+asyncpg://postgres:123@localhost:5432/postgres"

`SECRET` = "Brunchik"

`DB_HOST` = "localhost"

`DB_PORT` = "5432"

`DB_NAME` = "postgres"

`DB_USER` = "postgres"

`DB_USER` = "123"
## Запуск backend проекта

Переходим в каталог проекта

```bash
  cd backend
```

Установка зависимостей

```bash
  pip3 install -r requirements.txt
```

Применение миграций

```bash
  alembic upgrade head
```

Запуск проекта

```bash
  uvicorn app.main:app --reload
```

После запуска проект будет доступен по ссылке:
127.0.0.1:8000/docs#/


## Запуск frontend+backend проекта

Переходим в каталог с docker-compose

```bash
  cd infra
```

Запуск docker-compose

```bash
  docker-compose up -d --build
```

Применение миграций проекта

```bash
  docker-compose exec backend alembic upgrade head
```