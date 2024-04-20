from aiogram.types import InputMediaPhoto, InlineKeyboardMarkup, FSInputFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import CAPTIONS, OOPS_DIET
from app.crud import calorie_crud
from app.exceptions.calorie import NoCaloriePlot
from app.keyboards import get_calories_btns
from app.models import User
from app.utils.utils import (calculation_of_calories,
                             get_banner)


async def calorie_counter(
    level: int,
    menu_name: str,
    user: User,
    session: AsyncSession,
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    try:
        plot = await calorie_crud.get_plot(session, user)
    except NoCaloriePlot:
        return (
            await get_banner(OOPS_DIET, level=level),
            get_calories_btns(level=level),
        )
    return (
        InputMediaPhoto(
            media=FSInputFile(plot),
            caption=CAPTIONS[menu_name].format(
                await calculation_of_calories(user),
            ),
        ),
        get_calories_btns(level=level),
    )
