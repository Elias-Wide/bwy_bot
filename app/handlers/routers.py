from aiogram import Router

from app.handlers import (
    echo_router,
    settings_router,
    shedule_router,
    sleep_router,
    survey_router,
    user_router,
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
