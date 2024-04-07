from aiogram import Router

from app.handlers.callbacks import echo_router, user_router

main_router = Router()

main_router.include_router(user_router)
main_router.include_router(echo_router)
