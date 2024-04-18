from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import (
    CONFIRM,
    GENDER,
    INTRO_SURVEY_TEXT,
    SurveyQuestions,
)
from app.core.logging import get_logger
from app.crud import user_crud
from app.filters.survey_filters import (
    ExistingUserFilter,
    HumanParameterFilter,
    filter_invalid_email,
)
from app.keyboards import get_settings_btns
from app.keyboards.settings_kb import BUTTONS
from app.models import Schedule, User

router = Router()
logger = get_logger(__name__)


@router.callback_query(F.data == 'stop_train')
async def handle_survey_cancel(
    callback_query: CallbackQuery,
    session: AsyncSession,
) -> None:
    logger.info('TRAINNNNNN')


@router.callback_query(F.data == 'stop_sleep')
async def handle_survey_cancel(
    callback_query: CallbackQuery,
    session: AsyncSession,
) -> None:
    logger.info('SSSSSLEEP')


@router.callback_query(F.data == 'stop_calorie')
async def handle_survey_cancel(
    callback_query: CallbackQuery,
    session: AsyncSession,
) -> None:
    logger.info('CALORIES')
