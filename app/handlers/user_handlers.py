from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from handlers.menu_processor import get_menu_content


router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    """Хэндлер команды '/start'."""
    media, reply_markup = await get_menu_content(level=0, menu_name='main')
    await message.answer_photo(
        photo=media.media,
        caption=media.caption,
        reply_markup=reply_markup,
    )
