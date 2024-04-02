from fastapi import FastAPI
from aiogram import types
from app.bot import dp, bot, TOKEN
import logging
from app.core.config import settings


app = FastAPI()
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s',
)
logger.info('API is starting up')

WEBHOOK_PATH = f'/bot/{TOKEN}'
WEBHOOK_URL = f'{settings.webhook_url}{WEBHOOK_PATH}'


@app.on_event('startup')
async def on_startup() -> None:
    webhook_info = await bot.get_webhook_info()
    logger.info(webhook_info)
    if webhook_info.url != WEBHOOK_URL:
#        logger.info( WEBHOOK_URL)
        await bot.set_webhook(
            url=WEBHOOK_URL,
        )


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict) -> None:
    telegram_update = types.Update(**update)
    await dp.feed_update(bot=bot, update=telegram_update)


@app.on_event('shutdown')
async def on_shutdown() -> None:
    await bot.session.close()
