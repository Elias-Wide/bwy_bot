from fastapi import FastAPI
from aiogram import types, Bot, Dispatcher
from app.keyboards.main_menu import set_main_menu
from app.handlers import trainings_router

from pathlib import Path
from app.core.logging import get_logger
from app.core.config import settings

from app.handlers import trainings_router

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI()
logger = get_logger(__name__)
logger.info('API is starting up')

TOKEN = settings.telegram_bot_token
WEBHOOK_HOST = settings.webhook_host
WEBHOOK_PATH = f'/bot/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'
WEBHOOK_MODE = True

bot = Bot(token=TOKEN, parse_mode='HTML')
dp = Dispatcher()
dp.include_router(trainings_router)

if not WEBHOOK_MODE:
    @app.on_event('startup')
    async def on_startup() -> None:
        webhook_info = await bot.get_webhook_info()
        logger.info(WEBHOOK_URL)
        if webhook_info.url != WEBHOOK_URL:
            await bot.delete_webhook()
            logger.info(WEBHOOK_URL)
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

else:
    @app.on_event('startup')
    async def on_startup() -> None:
        logger.info(settings.telegram_bot_token)
        await set_main_menu(bot)
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
