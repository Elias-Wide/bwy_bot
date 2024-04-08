from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, InputMediaVideo, Message
from aiogram.utils.chat_action import ChatActionSender

from app.handlers.menu_processor import get_menu_content
from app.keyboards import MenuCallBack

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message) -> None:
    """Хэндлер команды '/start'."""
    media, reply_markup = await get_menu_content(level=0, menu_name='main')
    await message.answer_photo(
        photo=media.media,
        caption=media.caption,
        reply_markup=reply_markup,
    )


@router.callback_query(MenuCallBack.filter())
async def user_menu(
    callback: CallbackQuery,
    callback_data: MenuCallBack,
) -> None:
    media, reply_markup = await get_menu_content(
        level=callback_data.level,
        menu_name=callback_data.menu_name,
    )
    if isinstance(media, InputMediaVideo):
        async with ChatActionSender.upload_video(
            chat_id=callback.message.chat.id,
            bot=callback.bot,
        ):
            await callback.answer(text='Загрузка...', show_alert=True)
            await callback.message.edit_media(
                media=media,
                reply_markup=reply_markup,
            )
    else:
        await callback.message.edit_media(
            media=media,
            reply_markup=reply_markup,
        )
        await callback.answer()
