from aiogram.fsm.state import State, StatesGroup


class SurveyOrder(StatesGroup):
    consent_confirm = State()
    gender_question = State()
    physical_activity_question = State()
    purpose_question = State()
    height_question = State()
    weight_question = State()
    age_question = State()
    email_question = State()
    finished = State()
