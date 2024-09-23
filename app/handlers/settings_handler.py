"""Модуль с функциями настроек (вкл-откл) напоминаний."""

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import INTRO_SETTINGS_TEXT
from app.core.logging import get_logger
from app.crud import schedule_crud, user_crud
from app.keyboards import get_settings_btns
from app.utils.utils import get_reminder_state

router = Router()
logger = get_logger(__name__)


@router.callback_query(F.data == 'stop_train')
async def handle_settings_train(
    callback_query: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    """Включает, отключает напоминание о тренировке."""
    await schedule_crud.switch_reminder(
        callback_query.message.chat.id,
        'stop_reminder_train',
        session,
    )
    await update_state_in_caption(
        callback_query,
        session,
    )


@router.callback_query(F.data == 'stop_sleep')
async def handle_settings_sleep(
    callback_query: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    """Включает, отключает напоминание о сне."""
    await schedule_crud.switch_reminder(
        callback_query.message.chat.id,
        'stop_reminder_sleep',
        session,
    )
    await update_state_in_caption(
        callback_query,
        session,
    )


@router.callback_query(F.data == 'stop_calorie')
async def handle_settings_calories(
    callback_query: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    """Включает, отключает напоминание о питаниии."""
    await schedule_crud.switch_reminder(
        callback_query.message.chat.id,
        'stop_reminder_calories',
        session,
    )
    await update_state_in_caption(
        callback_query,
        session,
    )


async def update_state_in_caption(
    callback_query: CallbackQuery,
    session: AsyncSession,
) -> None:
    """Показывает (обновляет) состояние напоминаний (вкл-откл)."""
    user = await user_crud.get_by_attribute(
        'telegram_id',
        callback_query.from_user.id,
        session,
    )
    res = await get_reminder_state(user, session)
    await callback_query.message.edit_caption(
        caption=(f'{INTRO_SETTINGS_TEXT}\n' f'{res}'),
        reply_markup=get_settings_btns(level=0),
    )
