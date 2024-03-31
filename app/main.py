from fastapi import FastAPI
from aiogram import types, Dispatcher, Bot
from app.bot import dp, bot, TOKEN


app = FastAPI()
WEBHOOK_PATH = f'/bot/{TOKEN}'
WEBHOOK_URL = f'https://2933-109-173-73-0.ngrok-free.app{WEBHOOK_PATH}'


@app.on_event("startup")
async def on_startup():
#    print('start')
    webhook_info = await bot.get_webhook_info()
    print('webhook_info =', webhook_info )
    if webhook_info.url != WEBHOOK_URL:
        print('WEBHOOK_URL = ', WEBHOOK_URL)
        await bot.set_webhook(
            url=WEBHOOK_URL
        )


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    await dp.feed_update(bot=bot, update=telegram_update)

    
@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()
