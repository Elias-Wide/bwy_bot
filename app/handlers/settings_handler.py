from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.crud import schedule_crud
from app.handlers.callbacks.user_handlers import process_start_command

router = Router()
logger = get_logger(__name__)


@router.callback_query(F.data == 'stop_train')
async def handle_settings_train(
    callback_query: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    await schedule_crud.switch_reminder(
        callback_query.message.chat.id,
        'stop_reminder_train',
        session,
    )
    await return_to_main_menu(callback_query.message, state, session)


@router.callback_query(F.data == 'stop_sleep')
async def handle_settings_sleep(
    callback_query: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    await schedule_crud.switch_reminder(
        callback_query.message.chat.id,
        'stop_reminder_sleep',
        session,
    )
    await return_to_main_menu(callback_query.message, state, session)


@router.callback_query(F.data == 'stop_calorie')
async def handle_settings_calories(
    callback_query: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    await schedule_crud.switch_reminder(
        callback_query.message.chat.id,
        'stop_reminder_calories',
        session,
    )
    await return_to_main_menu(callback_query.message, state, session)


async def return_to_main_menu(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    await process_start_command(message, state, session)
