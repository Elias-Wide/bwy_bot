"""Фильтры участка анкеты."""

from aiogram.filters import BaseFilter
from aiogram.types import Message
from email_validator import EmailNotValidError, validate_email
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.crud.user import user_crud
from app.exceptions.survey_exceptions import DisallowedHumanParameterError
from app.validators.survey_validators import (
    validate_local_time,
    validate_number_value,
)

logger = get_logger(__name__)


class HumanParameterFilter(BaseFilter):
    """Класс фильтрующий вводимые параметры в анкете."""

    def __init__(self, parameter_range: tuple[int, int]) -> None:
        self.parameter_range = parameter_range

    async def __call__(
        self,
        message: Message,
    ) -> bool | dict[str, int | None]:
        """Метод проверяет мин-макс возможное значение."""
        try:
            return {
                'value': validate_number_value(
                    message.text,
                    self.parameter_range,
                ),
            }
        except DisallowedHumanParameterError as error:
            logger.warning(error)
            return False


class ExistingUserFilter(BaseFilter):
    """Класс фильтрующий уникальный тг id."""

    def __init__(self) -> None:
        pass

    async def __call__(
        self,
        message: Message,
        session: AsyncSession,
    ) -> bool | dict[str, int]:
        """Метод проверяет наличие tg id в БД."""
        telegram_id = message.from_user.id
        if not await user_crud.get_by_attribute(
            'telegram_id',
            telegram_id,
            session,
        ):
            return {'telegram_id': telegram_id}
        return False


def filter_invalid_email(message: Message) -> str | None:
    """фильтр на валиндность e-mail."""
    try:
        return validate_email(message.text).normalized
    except EmailNotValidError as error:
        logger.warning(error)
        return None


async def filter_invalid_local_time(message: Message) -> str | None:
    """Проверка на корректность ввода локального времени.

    Может быть -11 или +14 от UTC,
    минуты совпадают(редкие исключения не учитываем)
    """
    try:
        return {
            'location': validate_local_time(
                message.text,
                message.date.strftime("%H:%M:%S"),
            ),
        }
    except Exception as error:
        logger.warning(error)
        return None
