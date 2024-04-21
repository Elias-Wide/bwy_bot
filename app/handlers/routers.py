from aiogram import Router

from app.handlers import (
    feature/schedul_refact
    shedule_router,
    sleep_router,
    survey_router,
    user_router,
    echo_router,
)

main_router = Router()

main_router.include_routers(
    shedule_router,
    survey_router,
    user_router,
    sleep_router,
    settings_router,
    echo_router,
)
