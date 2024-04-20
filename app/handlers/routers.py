from aiogram import Router

from app.handlers import (
    echo_router,
    shedule_router,
    survey_router,
    user_router,
)

main_router = Router()

main_router.include_routers(
    shedule_router,
    survey_router,
    user_router,
    echo_router,
)
