from aiogram.filters import BaseFilter
from aiogram.types import Message
from email_validator import EmailNotValidError, validate_email

from app.core.logging import get_logger
from app.exceptions.survey_exceptions import DisallowedHumanParameterError
from app.validators.survey_validators import validate_number_value

logger = get_logger(__name__)


def filter_invalid_email(message: Message) -> str | None:
    try:
        return validate_email(message.text).normalized
    except EmailNotValidError as error:
        logger.warning(error)
        return None


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
