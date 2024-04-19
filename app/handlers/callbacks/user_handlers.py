from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaVideo, Message
from aiogram.utils.chat_action import ChatActionSender
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.crud.user import user_crud
from app.handlers.menu_processor import get_menu_content
from app.handlers.states import SurveyOrder
from app.keyboards import MenuCallBack

router = Router()

logger = get_logger(__name__)


@router.message(CommandStart(), SurveyOrder.finished)
async def process_start_command(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    """Хэндлер команды '/start'."""
    user = await user_crud.get_by_attribute(
        'telegram_id',
        message.chat.id,
        session,
    )
    media, reply_markup = await get_menu_content(
        level=0,
        menu_name='main',
        user=user,
        session=session,
    )
    await message.answer_photo(
        photo=media.media,
        caption=media.caption,
        reply_markup=reply_markup,
    )
    await state.clear()


@router.callback_query(MenuCallBack.filter())
async def user_menu(
    callback: CallbackQuery,
    callback_data: MenuCallBack,
    session: AsyncSession,
) -> None:
    user = await user_crud.get_by_attribute(
        'telegram_id',
        callback.from_user.id,
        session,
    )
    media, reply_markup = await get_menu_content(
        level=callback_data.level,
        menu_name=callback_data.menu_name,
        user=user,
        session=session,
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
