"""Основной модуль программы.

Создаются экземпляры бота и диспетчера, подключаем роутер,
запускается бот с помощью FastApi lifespan в асинхронном режиме.
Подключается база данных, логика аутентификации и админка.
"""

from contextlib import asynccontextmanager
from typing import Any

from aiogram import Bot, Dispatcher, types
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from sqladmin import Admin

from app.admin.auth import AdminAuth
from app.admin.view import (
    AdvertisementAdmin,
    CalorieAdmin,
    ExerciseAdmin,
    ScheduleAdmin,
    SleepAdmin,
    UserAdmin,
    WorkoutAdmin,
    WorkoutExerciseAdmin,
)
from app.core.config import settings
from app.core.constants import SCHEDULE_JOB_HOUR, UTC
from app.core.db import AsyncSessionLocal, engine
from app.core.logging import get_logger
from app.handlers.routers import main_router
from app.handlers.schedule_handler import (
    time_to_adv_hourly,
    time_to_calorie_hourly,
    time_to_sleep_hourly,
    time_to_training_hourly,
)
from app.keyboards.main_menu import set_main_menu
from app.middlewares import DbSessionMiddleware

logger = get_logger(__name__)

WEBHOOK_PATH = f'/bot/{settings.telegram_bot_token}'
WEBHOOK_URL = f'{settings.webhook_host}{WEBHOOK_PATH}'
WEBHOOK_MODE = settings.webhook_mode

bot = Bot(token=settings.telegram_bot_token, parse_mode='HTML')
dp = Dispatcher()
dp.update.middleware(DbSessionMiddleware(session_pool=AsyncSessionLocal))
dp.callback_query.middleware(CallbackAnswerMiddleware())
dp.include_router(main_router)


@asynccontextmanager
async def lifespan(application: FastAPI) -> Any:
    """Запуск бота в режиме webhook.

    Добавление заданий в бота по отслеживанию
    напоминаний о тренировках, сне, контроле калорий.
    """
    logger.info("🚀 Starting application")
    scheduler = AsyncIOScheduler(timezone=UTC)
    scheduler.start()
    scheduler.add_job(
        time_to_training_hourly,
        trigger='cron',
        hour=SCHEDULE_JOB_HOUR,
    )
    scheduler.add_job(
        time_to_calorie_hourly,
        trigger='cron',
        hour=SCHEDULE_JOB_HOUR,
    )
    scheduler.add_job(
        time_to_sleep_hourly,
        trigger='cron',
        hour=SCHEDULE_JOB_HOUR,
    )
    scheduler.add_job(
        time_to_adv_hourly,
        trigger='cron',
        hour=SCHEDULE_JOB_HOUR,
        minute='29',
    )
    try:
        await bot.set_webhook(
            url=WEBHOOK_URL,
            allowed_updates=dp.resolve_used_update_types(),
            drop_pending_updates=True,
        )
        logger.info('URL = %s', WEBHOOK_URL)
        await set_main_menu(bot)
    except Exception as e:
        logger.error(f"Can't set webhook - {e}")
    yield
    await bot.delete_webhook()
    logger.info("⛔ Stopping application")


app = FastAPI(
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None,
)
app.add_middleware(DBSessionMiddleware, db_url=settings.database_url)


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict) -> None:
    """Назначаем путь для обработки POST-запросов от телеграмма."""
    telegram_update = types.Update(**update)
    await dp.feed_webhook_update(bot=bot, update=telegram_update)


authentication_backend = AdminAuth(secret_key=settings.admin_auth_secret)
admin = Admin(
    app=app,
    engine=engine,
    authentication_backend=authentication_backend,
)
admin.add_view(UserAdmin)
admin.add_view(WorkoutAdmin)
admin.add_view(ExerciseAdmin)
admin.add_view(WorkoutExerciseAdmin)
admin.add_view(SleepAdmin)
admin.add_view(CalorieAdmin)
admin.add_view(ScheduleAdmin)
admin.add_view(AdvertisementAdmin)
