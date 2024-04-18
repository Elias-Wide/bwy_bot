from aiogram import Router

from app.handlers import survey_router
from app.handlers.callbacks import (
    echo_router, user_router, shedule_router
)

main_router = Router()

main_router.include_routers(
    shedule_router, survey_router, user_router, echo_router
)
