import asyncio
import logging
from pathlib import Path

from aiogram import Bot, Dispatcher

from keyboards.main_menu import set_main_menu
from handlers import trainings_router
from core.config import settings


BASE_DIR = Path(__file__).resolve().parent.parent

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s'
    )

    logger.info('Bot is running!')

    bot = Bot(token=settings.telegram_bot_token, parse_mode='HTML')
    dp = Dispatcher()

    dp.include_router(trainings_router)

    await set_main_menu(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
