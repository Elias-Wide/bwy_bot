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

- Запуск админки:

```shell
uvicorn app.main:app --reload
```

- Запуск бота:

```shell
python app/bot.py
```
