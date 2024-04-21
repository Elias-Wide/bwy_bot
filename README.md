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
WEBHOOK_MODE = 'True'
# из экрана запуска ndrok:
WEBHOOK_HOST = 'https://f8b9-109-173-73-0.ngrok-free.app' 

```

Если БД локально не существует команда для создания

```shell
alembic upgrade 76aa57ba6258  # это цифры последней ревизии 
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
