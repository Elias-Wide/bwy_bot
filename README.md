# begin_with_yourself_bot_2
Подготовка к запуску
- Создаем виртуальное окружение
```bash
python -m venv venv
```
- Активируем виртуальное окружение
```bash
source venv/bin/activate
```
- Формируем файлы requirements.txt
```bash
make dev-deps
```
- Устанавливаем зависимости (для разработки)

```bash
make install-dev-deps
```


Два варианта запуска бота.

1. fastapi + webhook (так будет на продакшн)
 - Устанавливаем ngrok.
 - настраиваем ngrok. (ссылки можно найти в Notions - Docs)
 - в файле .env переменные окружения : токен бота и адрес webhook из окошка ngrok

```
uvicorn app.main:app --reload
```
---------------------------

2. polling fastapi отдельно.

bot пока запускается через:
```
python bot_polling.py
```
или
```
python app/bot_polling.py
```

