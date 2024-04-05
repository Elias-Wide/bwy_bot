from aiogram import Bot, Dispatcher, types
from fastapi import FastAPI
from sqladmin import Admin

from app.admin.view import FileAdmin, UserAdmin

# from app.admin.auth import AdminAuth # to do
from app.core.config import settings
from app.core.db import engine
from app.core.logging import get_logger
from app.handlers import trainings_router
from app.keyboards.main_menu import set_main_menu

WEBHOOK_PATH = f'/bot/{settings.telegram_bot_token}'
WEBHOOK_URL = f'{settings.webhook_host}{WEBHOOK_PATH}'
WEBHOOK_MODE = settings.webhook_mode

app = FastAPI()
logger = get_logger(__name__)
logger.info('App starting up')

bot = Bot(token=settings.telegram_bot_token, parse_mode='HTML')
dp = Dispatcher()
dp.include_router(trainings_router)

admin = Admin(
    app=app,
    engine=engine,
    #    authentication_backend=authentication_backend # to do
)
admin.add_view(UserAdmin)
admin.add_view(FileAdmin)

if WEBHOOK_MODE:

    @app.on_event('startup')
    async def on_startup() -> None:
        webhook_info = await bot.get_webhook_info()
        logger.info(WEBHOOK_MODE)
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
        logger.info(settings.webhook_mode)
        logger.info(settings.telegram_bot_token)
        await set_main_menu(bot)
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
