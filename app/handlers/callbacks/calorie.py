from aiogram.types import InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import CAPTIONS
from app.keyboards import get_calories_btns
from app.models import User
from app.utils.utils import calculation_of_calories, get_calorie_plot


async def calorie_counter(
    level: int,
    menu_name: str,
    user: User,
    session: AsyncSession,
) -> tuple[InputMediaPhoto]:
    return (
        InputMediaPhoto(
            media=await get_calorie_plot(user, session),
            caption=CAPTIONS[menu_name].format(
                await calculation_of_calories(user),
            ),
        ),
        get_calories_btns(level=level),
    )
