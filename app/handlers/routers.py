from aiogram import Router

from app.handlers.callbacks import echo_router, survey_router, user_router

main_router = Router()

main_router.include_routers(survey_router, user_router, echo_router)
