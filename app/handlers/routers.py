from aiogram import Router

from app.handlers import survey_router
from app.handlers.callbacks import echo_router, user_router
from app.handlers import settings_router

main_router = Router()

main_router.include_routers(
    survey_router,
    user_router,
    settings_router,
    echo_router
)
