"""Модуль с функциями анкеты."""

from datetime import timedelta

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import (
    CallbackQuery,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import (
    ACTIVITY_KEYBOARD_SIZE,
    ACTIVITY_PURPOSE,
    ALLOWED_AGE_RANGE,
    ALLOWED_HEIGHT_RANGE,
    ALLOWED_WEIGHT_RANGE,
    CONFIRM,
    GENDER,
    HASH_PASSWORD,
    INTRO_SURVEY_TEXT,
    INVALID_EMAIL_MESSAGE,
    INVALID_NUM_MESSAGE,
    INVALID_TIME_MESSAGE,
    LOCATION,
    PHYSICAL_ACTIVITY,
    SHARE_LOCATION_BTN_TEXT,
    SURVEY_CANCELED,
    SURVEY_CONFIRMED,
    SURVEY_RESULT,
    SURVEY_TZ,
    SurveyQuestions,
)
from app.core.logging import get_logger
from app.crud import user_crud
from app.filters.survey_filters import (
    ExistingUserFilter,
    HumanParameterFilter,
    filter_invalid_email,
    filter_invalid_local_time,
)
from app.handlers.states import SurveyOrder
from app.handlers.user_handlers import process_start_command
from app.keyboards import create_survey_kb
from app.models import Schedule, User
from app.utils.survey import (
    get_possible_location,
    get_timezone_from_location,
    get_utc_offset,
)

router = Router()
logger = get_logger(__name__)


async def return_to_main_menu(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    """Возврат в главное меню."""
    await state.set_state(SurveyOrder.finished)
    await process_start_command(message, state, session)


@router.message(default_state, CommandStart(), ExistingUserFilter())
async def begin_survey(
    message: Message,
    state: FSMContext,
    telegram_id: int,
) -> None:
    """Приветствие и согласие ответить на вопросы."""
    await state.update_data(
        telegram_id=telegram_id,
        name=message.from_user.first_name,
    )
    await message.answer(
        text=f'{INTRO_SURVEY_TEXT}{SurveyQuestions.CONSENT}',
        reply_markup=await create_survey_kb(
            dict(CONFIRM).values(),
            dict(CONFIRM).keys(),
        ),
    )
    await state.set_state(SurveyOrder.consent_confirm)


@router.callback_query(F.data == SURVEY_CANCELED)
async def handle_survey_cancel(
    callback_query: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    """Отказ от анкетирования."""
    await state.set_state(SurveyOrder.finished)
    await return_to_main_menu(callback_query.message, state, session)


@router.callback_query(SurveyOrder.consent_confirm, F.data == SURVEY_CONFIRMED)
async def ask_gender(
    callback_query: CallbackQuery,
    state: FSMContext,
) -> None:
    """Вопрос про гендер, после согласия анкетироваться."""
    await callback_query.message.edit_text(
        text=SurveyQuestions.GENDER,
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
    """Сохранение гендера в state. Вопрос про активность."""
    await state.update_data(gender=callback_query.data)
    await callback_query.message.edit_text(
        text=SurveyQuestions.PHYSICAL_ACTIVITY,
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
    """Сохранение активности в state. Вопрос про цель."""
    await state.update_data(activity=callback_query.data)
    await callback_query.message.edit_text(
        text=SurveyQuestions.PURPOSE,
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
    """Сохранение цели в state. Вопрос про рост."""
    await state.update_data(purpose=callback_query.data)
    await callback_query.message.answer(
        text=SurveyQuestions.HEIGHT,
    )
    await state.set_state(SurveyOrder.height_question)


@router.message(
    SurveyOrder.height_question,
    HumanParameterFilter(ALLOWED_HEIGHT_RANGE),
)
async def ask_weight(message: Message, state: FSMContext, value: int) -> None:
    """Сохранение рост в state. Вопрос про вес."""
    await state.update_data(height=value)
    await message.answer(text=SurveyQuestions.WEIGHT)
    await state.set_state(SurveyOrder.weight_question)


@router.message(
    SurveyOrder.weight_question,
    HumanParameterFilter(ALLOWED_WEIGHT_RANGE),
)
async def ask_age(message: Message, state: FSMContext, value: int) -> None:
    """Сохранение веса в state. Вопрос про возраст."""
    await state.update_data(weight=value)
    await message.answer(text=SurveyQuestions.AGE)
    await state.set_state(SurveyOrder.age_question)


@router.message(
    SurveyOrder.age_question,
    HumanParameterFilter(ALLOWED_AGE_RANGE),
)
async def ask_geo(message: Message, state: FSMContext, value: int) -> None:
    """
    Сохранение возраста в state.

    Вопрос поделиться локацией или написать время.
    """
    await state.update_data(age=value)
    btn_lst = [
        [
            KeyboardButton(
                text=SHARE_LOCATION_BTN_TEXT,
                request_location=True,
            ),
        ],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=btn_lst,
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    await message.answer(
        text=SurveyQuestions.LOCATION,
        reply_markup=keyboard,
    )
    await state.set_state(SurveyOrder.location)


@router.message(SurveyOrder.location, filter_invalid_local_time)
async def ask_email(message: Message, state: FSMContext) -> None:
    """
    Сохранение локации в state.

    Вычисление utc_offset. Вопрос про email.
    """
    if message.location is not None:
        location_str = await get_timezone_from_location(
            message.location.longitude,
            message.location.latitude,
        )
    else:
        location_str = await get_possible_location(message.text, message.date)
    await state.update_data(location=location_str)
    await message.answer(
        text=(f'{SurveyQuestions.EMAIL}'),
    )
    await state.set_state(SurveyOrder.email_question)


@router.message(SurveyOrder.email_question, filter_invalid_email)
async def finish_survey(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    """
    Сохранение email в state.

    Запись инфо из state в БД. Завершение анкетирования.
    """
    await state.update_data(
        email=message.text,
        hashed_password=HASH_PASSWORD,
    )
    survey_result = await state.get_data()
    utc_offset = await get_utc_offset(survey_result[LOCATION])
    logger.info(
        await user_crud.create(
            User(
                **survey_result,
                schedule=[Schedule(utc_offset=utc_offset)],
            ),
            session,
        ),
    )
    td_str = (
        f'{SURVEY_TZ}'
        f'{"+ " if utc_offset>0 else ""}'
        f'{str(timedelta(seconds=utc_offset))}\n'
    )
    await message.answer(
        text=(f'{SURVEY_RESULT.format(**survey_result)}{td_str}'),
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(SurveyOrder.finished)
    await process_start_command(message, state, session)


@router.message(SurveyOrder.height_question)
async def handle_invalid_height_message(message: Message) -> None:
    """Сообщение о введенном невалидном росте."""
    await message.answer(
        text=INVALID_NUM_MESSAGE.format(*ALLOWED_HEIGHT_RANGE),
    )


@router.message(SurveyOrder.weight_question)
async def handle_invalid_weight_message(message: Message) -> None:
    """Сообщение о введенном невалидном весе."""
    await message.answer(
        text=INVALID_NUM_MESSAGE.format(*ALLOWED_WEIGHT_RANGE),
    )


@router.message(SurveyOrder.age_question)
async def handle_invalid_age_message(message: Message) -> None:
    """Сообщение о введенном невалидном возрасте."""
    await message.answer(
        text=INVALID_NUM_MESSAGE.format(*ALLOWED_AGE_RANGE),
    )


@router.message(SurveyOrder.location)
async def handle_invalid_locaion_message(message: Message) -> None:
    """Сообщение о введенном невалидной локации."""
    await message.answer(text=INVALID_TIME_MESSAGE.format(message.text))


@router.message(SurveyOrder.email_question)
async def handle_invalid_email_message(message: Message) -> None:
    """Сообщение о введенном невалидном email."""
    await message.answer(text=INVALID_EMAIL_MESSAGE)


@router.message(CommandStart(), ~ExistingUserFilter())
async def handle_existing_user(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    """Сообщение о уже существующем пользователе."""
    await state.set_state(SurveyOrder.finished)
    await return_to_main_menu(message, state, session)
