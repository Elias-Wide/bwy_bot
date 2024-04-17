from datetime import datetime

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import (
    ACTIVITY_PURPOSE,
    ALLOWED_AGE_RANGE,
    ALLOWED_HEIGHT_RANGE,
    ALLOWED_WEIGHT_RANGE,
    CONFIRM,
    GENDER,
    INTRO_SURVEY_TEXT,
    PHYSICAL_ACTIVITY,
    SURVEY_QUESTIONS,
)
from app.core.logging import get_logger
from app.crud.user import user_crud
from app.filters.survey_filters import (
    ExistingUserFilter,
    HumanParameterFilter,
    filter_invalid_email,
)
from app.keyboards import create_survey_kb, get_main_menu_btns
from app.models import Schedule, User

ACTIVITY_KEYBOARD_SIZE = (1,)
INVALID_NUM_MESSAGE = (
    'Введите целое число в диапазоне от {} до {} включительно'
)
INVALID_EMAIL_MESSAGE = 'Ошибка при вводе email. Попробуйте снова.'
START_URL = 't.me/{bot_username}?start=survey-canceled'
SURVEY_COMMAND = 'survey'
SURVEY_CONFIRMED, SURVEY_CANCELED = dict(CONFIRM).keys()
SURVEY_RESULT = '<b>Ваша анкета готова.</b>\n🎉\n{user_data}'

router = Router()
logger = get_logger(__name__)


class SurveyOrder(StatesGroup):
    consent_confirm = State()
    gender_question = State()
    physical_activity_question = State()
    purpose_question = State()
    height_question = State()
    weight_question = State()
    age_question = State()
    email_question = State()


@router.message(default_state, Command(SURVEY_COMMAND), ExistingUserFilter())
async def begin_survey(
    message: Message,
    state: FSMContext,
    telegram_id: int,
) -> None:
    await state.update_data(
        telegram_id=telegram_id,
        name=message.from_user.first_name,
    )
    await message.answer(
        text=INTRO_SURVEY_TEXT + SURVEY_QUESTIONS[0],
        reply_markup=await create_survey_kb(
            dict(CONFIRM).values(),
            dict(CONFIRM).keys(),
        ),
    )
    await state.set_state(SurveyOrder.consent_confirm)


@router.callback_query(F.data == SURVEY_CANCELED)
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


@router.callback_query(SurveyOrder.consent_confirm, F.data == SURVEY_CONFIRMED)
async def ask_gender(
    callback_query: CallbackQuery,
    state: FSMContext,
) -> None:
    await callback_query.message.edit_text(
        text=SURVEY_QUESTIONS[1],
        reply_markup=await create_survey_kb(
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
        text=SURVEY_QUESTIONS[2],
        reply_markup=await create_survey_kb(
            dict(PHYSICAL_ACTIVITY).values(),
            dict(PHYSICAL_ACTIVITY).keys(),
            ACTIVITY_KEYBOARD_SIZE,
        ),
    )
    await state.set_state(SurveyOrder.physical_activity_question)


@router.callback_query(
    SurveyOrder.physical_activity_question,
    F.data.in_(dict(PHYSICAL_ACTIVITY).keys()),
)
async def ask_purpose(
    callback_query: CallbackQuery,
    state: FSMContext,
) -> None:
    await state.update_data(activity=callback_query.data)
    await callback_query.message.edit_text(
        text=SURVEY_QUESTIONS[3],
        reply_markup=await create_survey_kb(
            dict(ACTIVITY_PURPOSE).values(),
            dict(ACTIVITY_PURPOSE).keys(),
        ),
    )
    await state.set_state(SurveyOrder.purpose_question)


@router.callback_query(
    SurveyOrder.purpose_question,
    F.data.in_(dict(ACTIVITY_PURPOSE).keys()),
)
async def ask_height(
    callback_query: CallbackQuery,
    state: FSMContext,
) -> None:
    await state.update_data(purpose=callback_query.data)
    await callback_query.message.edit_text(
        text=SURVEY_QUESTIONS[4],
        reply_markup=None,
    )
    await state.set_state(SurveyOrder.height_question)


@router.message(
    SurveyOrder.height_question,
    HumanParameterFilter(ALLOWED_HEIGHT_RANGE),
)
async def ask_weight(message: Message, state: FSMContext, value: int) -> None:
    await state.update_data(height=value)
    await message.answer(text=SURVEY_QUESTIONS[5])
    await state.set_state(SurveyOrder.weight_question)


@router.message(
    SurveyOrder.weight_question,
    HumanParameterFilter(ALLOWED_WEIGHT_RANGE),
)
async def ask_age(message: Message, state: FSMContext, value: int) -> None:
    await state.update_data(weight=value)
    await message.answer(text=SURVEY_QUESTIONS[6])
    await state.set_state(SurveyOrder.age_question)


@router.message(
    SurveyOrder.age_question,
    HumanParameterFilter(ALLOWED_AGE_RANGE),
)
async def ask_email(message: Message, state: FSMContext, value: int) -> None:
    await state.update_data(age=value)
    await message.answer(text=SURVEY_QUESTIONS[7])
    await state.set_state(SurveyOrder.email_question)


@router.message(SurveyOrder.email_question, filter_invalid_email)
async def finish_survey(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    await state.update_data(
        email=message.text,
        hashed_password='nkajipfncu89288)*&^guyb',
    )
    survey_result = await state.get_data()
    await message.answer(
        text=SURVEY_RESULT.format(user_data=survey_result),
        reply_markup=get_main_menu_btns(level=0),
    )

    user = await user_crud.create(
        User(
            **survey_result,
            schedule=[Schedule(start_course=datetime.now())],
        ),
        session,
    )
    logger.info(user)

    await state.clear()


@router.message(SurveyOrder.height_question)
async def handle_invalid_height_message(message: Message) -> None:
    await message.answer(
        text=INVALID_NUM_MESSAGE.format(*ALLOWED_HEIGHT_RANGE),
    )


@router.message(SurveyOrder.weight_question)
async def handle_invalid_weight_message(message: Message) -> None:
    await message.answer(
        text=INVALID_NUM_MESSAGE.format(*ALLOWED_WEIGHT_RANGE),
    )


@router.message(SurveyOrder.age_question)
async def handle_invalid_age_message(message: Message) -> None:
    await message.answer(
        text=INVALID_NUM_MESSAGE.format(*ALLOWED_AGE_RANGE),
    )


@router.message(SurveyOrder.email_question)
async def handle_invalid_email_message(message: Message) -> None:
    await message.answer(text=INVALID_EMAIL_MESSAGE)
