from aiogram.filters import BaseFilter
from aiogram.types import Message
from email_validator import EmailNotValidError, validate_email
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.crud.user import user_crud
from app.exceptions.survey_exceptions import DisallowedHumanParameterError
from app.validators.survey_validators import validate_number_value

logger = get_logger(__name__)


class HumanParameterFilter(BaseFilter):
    def __init__(self, parameter_range: tuple[int, int]) -> None:
        self.parameter_range = parameter_range

    async def __call__(
        self,
        message: Message,
    ) -> bool | dict[str, int | None]:
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
    def __init__(self) -> None:
        pass

    async def __call__(
        self,
        message: Message,
        session: AsyncSession,
    ) -> bool | dict[str, int]:
        telegram_id = message.from_user.id
        if (
            await user_crud.get_by_attribute(
                'telegram_id',
                telegram_id,
                session,
            )
            is None
        ):
            return {'telegram_id': telegram_id}
        return False


def filter_invalid_email(message: Message) -> str | None:
    try:
        return validate_email(message.text).normalized
    except EmailNotValidError as error:
        logger.warning(error)
        return None
