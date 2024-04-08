from aiogram import F, Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.data.survey import (
    GENDER,
    PHYSICAL_ACTIVITY,
    PURPOSE,
    SURVEY_QUESTIONS,
)
from app.keyboards import create_mode_kb, create_survey_kb

router = Router()


class OrderSurvey(StatesGroup):
    gender_question = State()
    height_question = State()
    weight_question = State()
    age_question = State()
    physical_activity_question = State()
    purpose_question = State()


@router.message(StateFilter(None), F.text.lower() == 'анкетирование')
async def begin_survey(message: types.Message, state: FSMContext) -> None:
    await message.answer(
        text=SURVEY_QUESTIONS[0],
        reply_markup=await create_survey_kb(GENDER),
    )
    await state.set_state(OrderSurvey.gender_question)


@router.message(OrderSurvey.gender_question, F.text.in_(GENDER))
async def answer_height(message: types.Message, state: FSMContext) -> None:
    await state.update_data(gender=message.text.lower())
    await message.answer(
        text=SURVEY_QUESTIONS[1],
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await state.set_state(OrderSurvey.height_question)


@router.message(OrderSurvey.height_question)
async def answer_weight(message: types.Message, state: FSMContext) -> None:
    await state.update_data(height=message.text.lower())
    await message.answer(
        text=SURVEY_QUESTIONS[2],
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await state.set_state(OrderSurvey.weight_question)


@router.message(OrderSurvey.weight_question)
async def answer_age(message: types.Message, state: FSMContext) -> None:
    await state.update_data(weight=message.text.lower())
    await message.answer(
        text=SURVEY_QUESTIONS[3],
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await state.set_state(OrderSurvey.age_question)


@router.message(OrderSurvey.age_question)
async def answer_activity(message: types.Message, state: FSMContext) -> None:
    await state.update_data(age=message.text.lower())
    await message.answer(
        text=SURVEY_QUESTIONS[4],
        reply_markup=await create_survey_kb(PHYSICAL_ACTIVITY),
    )
    await state.set_state(OrderSurvey.physical_activity_question)


@router.message(
    OrderSurvey.physical_activity_question,
    F.text.in_(PHYSICAL_ACTIVITY),
)
async def answer_purpose(message: types.Message, state: FSMContext) -> None:
    await state.update_data(physical_activity=message.text.lower())
    await message.answer(
        text=SURVEY_QUESTIONS[5],
        reply_markup=await create_survey_kb(PURPOSE),
    )
    await state.set_state(OrderSurvey.purpose_question)


@router.message(
    OrderSurvey.purpose_question,
    F.text.in_(PURPOSE),
)
async def finish_survey(message: types.Message, state: FSMContext) -> None:
    await state.update_data(purpose=message.text.lower())
    user_data = await state.get_data()
    await message.answer(
        text=f'Ваша анкета готова.\n\n{user_data}',
        reply_markup=await create_mode_kb(),
    )
    await state.clear()
