from aiogram import Router
from aiogram.types import Message

from app.core.constants import INTRO_SLEEP_TEXT
from app.keyboards import MenuCallBack

router = Router()


@router.message(MenuCallBack.filter())
async def sleep_main_menu(message: Message) -> None:
    await message.answer(text=INTRO_SLEEP_TEXT)
