from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.types import CallbackQuery, Message

from app.core.constants import (
    CONFIRM,
    GENDER,
    INTRO_SLEEP_TEXT,
    SLEEP_MAIN_MENU,
)
from app.filters.survey_filters import (
    HumanParameterFilter,
    filter_invalid_email,
)
from app.keyboards import create_sleep_kb, get_main_menu_btns
from app.core.logging import get_logger

logger = get_logger(__name__)

START_URL = 't.me/{bot_username}?start=sleep-canceled'
ACTIVITY_KEYBOARD_SIZE = (1,)
INVALID_NUM_MESSAGE = (
    'Введите целое число в диапазоне от {} до {} включительно'
)
SLEEP_COMMAND = 'sleep'
GO_TO_BED, WAKE_UP, SLEEP_DURATION, SLEEP_SATISTIC = dict(SLEEP_MAIN_MENU).keys()
SLEEP_CONFIRMED, SLEEP_CANCELED = dict(CONFIRM).keys()


router = Router()


class SurveyOrder(StatesGroup):
    consent_confirm = State()
    gender_question = State()
    physical_activity_question = State()
    purpose_question = State()
    height_question = State()
    weight_question = State()
    age_question = State()
    email_question = State()


@router.message(default_state, Command(SLEEP_COMMAND))
async def sleep_main_menu(message: Message, state: FSMContext) -> None:
    logger.info(message)
    await message.answer(
        text=INTRO_SLEEP_TEXT,
        reply_markup=await create_sleep_kb(
            dict(SLEEP_MAIN_MENU).values(),
            dict(SLEEP_MAIN_MENU).keys(),
        ),
    )
    await state.set_state(SurveyOrder.consent_confirm)


@router.callback_query(F.data == GO_TO_BED)
async def return_to_main_menu(
    callback_query: CallbackQuery,
    state: FSMContext,
) -> None:
    await state.clear()
    await callback_query.answer(
        url=START_URL.format(
            bot_username=(await callback_query.bot.me()).username,
        ),
    )


@router.callback_query(SurveyOrder.consent_confirm, F.data == SLEEP_CONFIRMED)
async def ask_gender(
    callback_query: CallbackQuery,
    state: FSMContext,
) -> None:
    await state.update_data(survey_confirmed=callback_query.data)
    await callback_query.message.edit_text(
        text='Потом добавлю',
        reply_markup=await create_sleep_kb(
            dict(GENDER).values(),
            dict(GENDER).keys(),
        ),
    )
    await state.set_state(SurveyOrder.gender_question)


@router.callback_query(
    SurveyOrder.gender_question,
    F.data.in_(dict(GENDER).keys()),
)
async def ask_activity(
    callback_query: CallbackQuery,
    state: FSMContext,
) -> None:
    await state.update_data(gender=callback_query.data)
    await callback_query.message.edit_text(
        text='Потом доб',
        reply_markup=await create_sleep_kb(
            dict(SLEEP_CONFIRMED).values(),
            dict(SLEEP_CONFIRMED).keys(),
            ACTIVITY_KEYBOARD_SIZE,
        ),
    )
    await state.set_state(SurveyOrder.physical_activity_question)
