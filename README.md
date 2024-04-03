# begin_with_yourself_bot_2

## Запуск на Linux в dev-режиме

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

- Запуск бота в режиме POLLING(устаревший)

```shell
python app/bot.py
```

 - Запск бота в режиме  POLLING
 
 в файле .env

```shell 
 WEBHOOK_MODE = 'False'
```

 ```shell
 uvicorn app.main:app
 ```

 - Запск бота в режиме  WEBHOOK:

установка навтройка ngrok

в файле .env:

```shell 
 WEBHOOK_MODE = 'True'
 WEBHOOK_HOST = 'https://f8b9-109-173-73-0.ngrok-free.app' # из экрана запуска ndrok
```

 ```shell
 uvicorn app.main:app --reload
 ```

Пример переменных окружения в .env.example
Для смены WEBHOOK_MODE нужно перезапустить термнал в котором запускали uvicorn или обновить переменные окружения.