from aiogram.types import FSInputFile

from app.core.config import BASE_DIR, UPLOAD_DIR
from app.core.constants import PHYS_ACTIV_KOEF
from app.models.user import User


async def _get_videos() -> list[FSInputFile]:
    return [FSInputFile(path) for path in list(UPLOAD_DIR.glob('*.mp4'))]


# TODO: exception.TelegramBadRequest: PHOTO_INVALID_DIMENSIONS
async def _get_banner(menu_name: str) -> FSInputFile:
    return FSInputFile(BASE_DIR.joinpath('static', menu_name + '.jpg'))


# TODO: продумать момент хранения графиков каллоража/ директория/ названия
async def _get_calorie_plot() -> FSInputFile:
    return FSInputFile(
        BASE_DIR.joinpath('static/calorie_plots', 'plot' + '01' + '.jpg'),
    )


async def _calculation_of_calories(user: User) -> int:
    if user.gender == 'MALE':
        res = (88.36 + (13.4 * user.weight)
               + (4.8 * user.height) - (5.7 * user.age))
    else:
        res = (447.6 + (9.2 * user.weight)
               + (3.1 * user.height) - (4.3 * user.age))
    return round(res * PHYS_ACTIV_KOEF[user.activity], 2)
