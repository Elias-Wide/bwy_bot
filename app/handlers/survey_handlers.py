from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.types import CallbackQuery, Message

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
from app.filters.survey_filters import (
    filter_invalid_age,
    filter_invalid_email,
    filter_invalid_height,
    filter_invalid_weight,
)
from app.keyboards import create_survey_kb, get_main_menu_btns

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


class SurveyOrder(StatesGroup):
    consent_confirm = State()
    gender_question = State()
    physical_activity_question = State()
    purpose_question = State()
    height_question = State()
    weight_question = State()
    age_question = State()
    email_question = State()


@router.message(default_state, Command(SURVEY_COMMAND))
async def begin_survey(message: Message, state: FSMContext) -> None:
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
    await state.update_data(survey_confirmed=callback_query.data)
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
    await state.update_data(physical_activity=callback_query.data)
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
    await state.update_data(activity_purpose=callback_query.data)
    await callback_query.message.edit_text(
        text=SURVEY_QUESTIONS[4],
        reply_markup=None,
    )
    await state.set_state(SurveyOrder.height_question)


@router.message(SurveyOrder.height_question, filter_invalid_height)
async def ask_weight(message: Message, state: FSMContext) -> None:
    await state.update_data(height=int(message.text))
    await message.answer(text=SURVEY_QUESTIONS[5])
    await state.set_state(SurveyOrder.weight_question)


@router.message(SurveyOrder.weight_question, filter_invalid_weight)
async def ask_age(message: Message, state: FSMContext) -> None:
    await state.update_data(weight=int(message.text))
    await message.answer(text=SURVEY_QUESTIONS[6])
    await state.set_state(SurveyOrder.age_question)


@router.message(SurveyOrder.age_question, filter_invalid_age)
async def ask_email(message: Message, state: FSMContext) -> None:
    await state.update_data(age=int(message.text))
    await message.answer(text=SURVEY_QUESTIONS[7])
    await state.set_state(SurveyOrder.email_question)


@router.message(SurveyOrder.email_question, filter_invalid_email)
async def finish_survey(message: Message, state: FSMContext) -> None:
    await state.update_data(
        email=message.text,
        telegram_id=message.from_user.id,
        name=message.from_user.first_name,
    )
    await message.answer(
        text=SURVEY_RESULT.format(user_data=await state.get_data()),
        reply_markup=get_main_menu_btns(level=0),
    )
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
