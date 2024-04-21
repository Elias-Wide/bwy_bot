# begin_with_yourself_bot_2

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

- Установите зависимости

```shell
make dev-deps && make install-dev-deps
```


 - Запуск бота в режиме  POLLING
 
 в файле .env

```text
 WEBHOOK_MODE = 'False'
```

 ```shell
 uvicorn app.main:app
 ```

 - Запуск бота в режиме WEBHOOK(рекомендуемый):

установка наcтройка ngrok

в файле .env:

```text
TELEGRAM_BOT_TOKEN = '***********:***************************'
WEBHOOK_HOST = 'https://*******************.ngrok-free.app'
WEBHOOK_MODE = 'False'
DATABASE_URL = 'sqlite+aiosqlite:///./bwy_bot.db'
# DATABASE_URL = "postgresql:////user:password@postgresserver/db"
USERNAME = 'mail@mail.ru'
PASSWORD = 'S0me-Passwd-123'
ADMIN_AUTH_SECRET = 'Some_Secret_Sting!' 

```

Если БД локально не существует команда для создания

```shell
alembic upgrade 80fd02331d15  # это цифры последней ревизии 
```

```shell
uvicorn app.main:app --reload
```

Пример переменных окружения в .env.example.
Для смены WEBHOOK_MODE нужно перезапустить терминал в котором 
запускали uvicorn или обновить переменные окружения.

Если перезапускали ngrok, проверьте изменилась ли переменная 
WEBHOOK_HOST и после изменемия ее в .env нужно перезапустить терминал
в котором запускали uvicorn или обновить переменные окружения.


=========================================
Один из вариантов (простой деплой) на сервер:

- Выполняем все вышеописанное кроме установливки ngrok, 
- На сервере переключаем в файле .env 

```text
WEBHOOK_MODE = 'True'
WEBHOOK_HOST = 'https://<имя Вашего домена>'
```

Конфигурируем nginx, если используется. Пример в default.nginx.example.

```shell
(venv) $ sudo vim /etc/nginx/sites-available/<имя Вашего домена>
(venv) $ sudo ln -s /etc/nginx/sites-available/<имя Вашего домена> /etc/nginx/sites-enabled/
(venv) $ sudo systemctl restart nginx.service
```

Строка запуска на сервере вручную для проверки чуть другая:

```shell
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8888
```

Добавляем приложение в службы для автоматического запуска.
Используем ASGI Server. Пример в bwy.service.example.

```shell
(venv) $ deactivate
$ sudo vim /etc/systemd/system/bwy.service
$ sudo systemctl start myapp.service
```

