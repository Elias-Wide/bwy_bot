# begin_with_yourself_bot_2 
# Телеграм-бот "Начни с себя"

## Назначение:
Помощь людям на начальных этапах пути к телу своей мечты.

Бот начинает с вводного приветствия и небольшого анкетирования, чтобы узнать потребности клиента и подсказать ему программу питания, сна, тренировок и т.д. исходя из индивидуальных потребностей. Уведомления-напоминания о тренировках, приеме пищи, сне. В режиме «тренировка» бот пошагово говорит какие упражнения делать, присылая видео с техникой выполнения упражнения, кол-вом повторений. У пользователя имеется возможность управления напоминаниями (отключение части напоминаний или всех)
Администрирование осуществляется через административный раздел сайта, стартующий вместе с ботом. Через него осуществляется наполнение БД, видео по упражнениям, картинками (диаграммы КБЖУ) и составляется программа тренировок, и другое управление содержимым бота. Имеется возможность дополнительных анонсов (картинка, текст, HTML)
БД наполнена только примерами упражнений и тренировок для случая заполненой анкеты - мужчина, сброс массы.

## Cтек:

![](https://img.shields.io/badge/Python-Version:_3.10.13-blue?logo=python&style=plastic)
![](https://img.shields.io/badge/FastAPI-Version:_0.110.0-blue?logo=fastapi&style=plastic)
![](https://img.shields.io/badge/Aiogram-Version:_3.4.1-blue?logo=fastapi&style=plastic)
![](https://img.shields.io/badge/SQLAlchemy-Version:_2.0.29-blue?logo=sqlalchemy&style=plastic)
![](https://img.shields.io/badge/Aiosqlite-Version:_0.20.0-blue?logo=apscedule&style=plastic)
![](https://img.shields.io/badge/Sqladmin-Version:_0.16.1-blue?logo=apscedule&style=plastic)
![](https://img.shields.io/badge/Pydantic-Version:_2.2.1-blue?logo=pydantic&style=plastic)
![](https://img.shields.io/badge/Alembic-Version:_1.13.1-blue?logo=alembic&style=plastic)
![](https://img.shields.io/badge/APScheduler-Version:_7.4.2-blue?logo=apscedule&style=plastic)
![](https://img.shields.io/badge/Pytz-Version:_2024.1-blue?logo=apscedule&style=plastic)
![](https://img.shields.io/badge/Gunicorn-Version:_22.0.0-blue?logo=apscedule&style=plastic)
![](https://img.shields.io/badge/Uvicorn-Version:_0.17.6-blue?logo=uvicorn&style=plastic)

## Запуск на Linux, Macos в dev-режиме

- Склонируйте репозиторий и перейдите в директорию проекта

```shell
git clone \
https://github.com/Studio-Yandex-Practicum/begin_with_yourself_bot_2.git && \
cd begin_with_yourself_bot_2
```

- Установите и активируйте виртуальное окружение

```shell
python -m venv venv && source venv/bin/activate
```

- Установите зависимости с помощью setuptools >= 61.0

```shell
make dev-deps && make install-dev-deps
```

 - Запуск бота:

Локально запустить в режиме WEBHOOK не получится без установки ngrok, режим POLLING не предусмотрен. Установка наcтройка ngrok ( см. в интернет https://losst.pro/kak-polzovatsya-ngrok ) нужна для форвардинга порта localhost:8000 (FastAPI) в интернет с присвоением ему публичного динамического DNS имени.

* в файле .env:

```text
TELEGRAM_BOT_TOKEN = '1234567890:Ваш_телеграм_токен'
WEBHOOK_HOST = 'https://внешний_адрес_forwarding.ngrok-free.app'
WEBHOOK_MODE = 'True'
DATABASE_URL = 'sqlite+aiosqlite:///./bwy_bot.db'
# DATABASE_URL = "postgresql:////user:password@postgresserver/db"
USERNAME = 'mail@mail.ru'
PASSWORD = 'S0me-Passwd-123'
ADMIN_AUTH_SECRET = 'Some_Secret_Sting!' 

```
Пример переменных окружения см. в .env.example.

USERNAME, PASSWORD для доступа в админку по адресу http://localhost:8000.
* Если БД не существует команда для создания:

```shell
alembic upgrade 6642ff71df04  # это цифры последней ревизии 
```

* Cобственно запуск:

```shell
uvicorn app.main:app --reload
```

## Запуск в docker - контейнере.

* Скачиваем устанавливаем docker https://www.docker.com/
* Скачиваем устанавливаем ngrok.
* Не забываем в файле .env 

```text
WEBHOOK_HOST = 'https://внешний_адрес_forwarding.ngrok-free.app'
```

* Cборка образа, запуск в контейнере:

```shell
docker build -t bwy_image .
docker run -d --name bwy_container -p 8000:8000 bwy_image
```

* Остановить контейнер:

```shell
docker stop bwy_container
```

 ## Один из вариантов (простой деплой) на сервер (Ubuntu):

* Выполняем все вышеописанное кроме установки ngrok, 
* На сервере в файле .env 

```text
WEBHOOK_HOST = 'https://<имя Вашего домена>'
```

Конфигурируем nginx, если используется. Пример в default.nginx.example.

```shell
(venv) $ sudo vim /etc/nginx/sites-available/<имя Вашего домена>
(venv) $ sudo ln -s /etc/nginx/sites-available/<имя Вашего домена> /etc/nginx/sites-enabled/
(venv) $ sudo systemctl restart nginx.service
```

Строка запуска на сервере вручную для проверки:

```shell
(venv) $ gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8888
```

* Добавляем приложение в службы для автоматического запуска.
Используем ASGI Server. Пример в bwy.service.example.

```shell
(venv) $ deactivate
$ sudo vim /etc/systemd/system/bwy.service
$ sudo systemctl start myapp.service
```

Удачи!

## Команда

* [**Дмитрий Красиков**](https://github.com/Krasikoff)
* [**Алена Перова**](https://github.com/AIPerova)
* [**Евгений Хлебнев**](https://github.com/Evgenmater)
* [**Максим Курмазов**](https://github.com/MaksimKurmazov)
* [**Олег Сапожников**](https://github.com/mign0n)
* [**Александр Роль**](https://github.com/RolAlek)
* [**Илья Широков**](https://github.com/Elias-Wide)
