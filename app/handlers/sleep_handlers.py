from aiogram import Router
from aiogram.types import Message

from app.keyboards import MenuCallBack
from app.utils.const import INTRO_SLEEP_TEXT

router = Router()


@router.message(MenuCallBack.filter())
async def sleep_main_menu(message: Message) -> None:
    await message.answer(text=INTRO_SLEEP_TEXT)
