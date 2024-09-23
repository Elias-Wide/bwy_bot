"""Модуль с функциями участка сна."""

from datetime import datetime, timedelta, timezone

from aiogram import F, Router
from aiogram.types import (
    CallbackQuery,
    FSInputFile,
    InlineKeyboardMarkup,
    InputMediaPhoto,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import STATIC_DIR
from app.core.constants import FMT_JPG, OOPS, SECONDS_IN_HOUR, SLEEP, SleepMode
from app.crud import sleep_crud, user_crud
from app.keyboards import MenuCallBack, get_oops_kb
from app.keyboards.sleep_kb import (
    get_sleep_back_btns,
    get_sleep_back_btns_duration,
    get_sleep_exist_btns,
    get_sleep_select_btns,
    get_sleep_statistic_btns,
    get_wake_up_btns,
)
from app.models import Sleep, User
from app.utils.sleep import (
    get_default_time,
    get_sleep_statistic_answer,
    get_sleep_status,
    get_yesterday,
)
from app.utils.survey import get_utc_offset
from app.utils.utils import get_banner

router = Router()


async def sleep_mode_menu(
    level: int,
    menu_name: str,
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    """Главное меню участка сна."""
    return (
        await get_banner(menu_name=menu_name),
        get_sleep_select_btns(level=level),
    )


async def go_to_bed_menu(
    level: int,
    menu_name: str,
    user: User,
    session: AsyncSession,
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    """Ответ времени отхода ко сну."""
    utc_offset_hours = await get_utc_offset(user.location) / SECONDS_IN_HOUR
    current_sleep_obj = await sleep_crud.get_last_sleep_obj(
        session=session,
        user=user,
    )
    sleep_status = await get_sleep_status(
        current_sleep_obj,
        int(utc_offset_hours),
        SleepMode.GO_TO_BED,
    )
    match sleep_status:
        case SleepMode.SLEEP_EXIST:
            menu_name = SleepMode.SLEEP_EXIST
        case SleepMode.FORGOT_SET_WKUP_TIME:
            menu_name = SleepMode.FORGOT_SET_WKUP_TIME
        case SleepMode.NOT_TIME_GTB:
            menu_name = SleepMode.NOT_TIME_GTB
        case SleepMode.VALID:
            return (
                await get_banner(
                    menu_name=menu_name,
                    utc_offset_hours=int(utc_offset_hours),
                ),
                get_sleep_back_btns(user=user, level=level),
            )
    return (
        await get_banner(
            menu_name=menu_name,
            utc_offset_hours=int(utc_offset_hours),
        ),
        await get_sleep_exist_btns(level=level),
    )


async def wake_up_menu(
    level: int,
    menu_name: str,
    user: User,
    session: AsyncSession,
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    """Ответ времени пробуждения."""
    utc_offset_hours = await get_utc_offset(user.location) / SECONDS_IN_HOUR
    current_sleep_obj = await sleep_crud.get_last_sleep_obj(
        session,
        user,
    )
    sleep_status = await get_sleep_status(
        current_sleep_obj,
        int(utc_offset_hours),
        SleepMode.WAKE_UP,
    )
    match sleep_status:
        case SleepMode.SLEEP_EXIST:
            menu_name = SleepMode.SLEEP_EXIST
        case SleepMode.FORGOT_SET_WKUP_TIME:
            menu_name = SleepMode.FORGOT_SET_WKUP_TIME
        case SleepMode.NOT_TIME_WKUP:
            menu_name = SleepMode.NOT_TIME_WKUP
        case SleepMode.VALID:
            return (
                await get_banner(
                    menu_name=menu_name,
                    utc_offset_hours=int(utc_offset_hours),
                ),
                get_wake_up_btns(level=level),
            )
    return (
        await get_banner(
            menu_name=menu_name,
            utc_offset_hours=int(utc_offset_hours),
        ),
        await get_sleep_exist_btns(level=level),
    )


async def sleep_duration_menu(
    level: int,
    menu_name: str,
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    """Ввод продолжительности сна."""
    return (
        await get_banner(menu_name),
        get_sleep_back_btns_duration(level=level),
    )


async def sleep_statistic_menu(
    level: int,
    menu_name: str,
    user: User,
    session: AsyncSession,
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    """Получение статистики сна за неделю."""
    sleeps = await sleep_crud.get_user_sleep_objs(user, 7, session)
    res = get_sleep_statistic_answer(sleeps)
    try:
        image = FSInputFile(STATIC_DIR.joinpath(menu_name + FMT_JPG))
    except Exception:
        return (
            await get_banner(OOPS, level),
            get_oops_kb(level=level, menu_name=menu_name),
        )
    return (
        InputMediaPhoto(
            media=image,
            caption=(f'\n {res}'),
        ),
        get_sleep_statistic_btns(level=level),
    )


@router.callback_query(MenuCallBack.filter(F.ok == SleepMode.GO_SLEEP_OK_BTN))
async def sleep_callback(
    callback_query: CallbackQuery,
    session: AsyncSession,
) -> None:
    """Ответ времени отхода ко сну заносим в БД."""
    user = await user_crud.get_by_attribute(
        'telegram_id',
        callback_query.from_user.id,
        session,
    )
    utc_offset_hours = await get_utc_offset(user.location) / SECONDS_IN_HOUR
    await sleep_crud.create(
        Sleep(
            user_id=user.id,
            go_to_bed_time=datetime.now(
                timezone(timedelta(hours=utc_offset_hours)),
            ),
            sleep_duration=0,
        ),
        session,
    )
    media, reply_markup = await sleep_mode_menu(
        level=1,
        menu_name=SLEEP,
    )
    await callback_query.message.answer_photo(
        text='DREAM',
        photo=media.media,
        caption=media.caption,
        reply_markup=reply_markup,
    )


@router.callback_query(MenuCallBack.filter(F.ok == SleepMode.WAKE_UP_OK_BTN))
async def wake_up_callback(
    callback_query: CallbackQuery,
    session: AsyncSession,
) -> None:
    """Ответ времени подьема заносим в БД."""
    user = await user_crud.get_by_attribute(
        'telegram_id',
        callback_query.from_user.id,
        session,
    )
    uts_offset_hours = await get_utc_offset(user.location) / SECONDS_IN_HOUR
    wake_up_time = datetime.now(timezone(timedelta(hours=uts_offset_hours)))
    await sleep_crud.set_wake_up_time(session, user, wake_up_time)
    media, reply_markup = await sleep_mode_menu(
        level=1,
        menu_name=SLEEP,
    )
    await callback_query.message.answer_photo(
        photo=media.media,
        caption=media.caption,
        reply_markup=reply_markup,
    )


@router.callback_query(MenuCallBack.filter(F.ok == SleepMode.DURATION_BTN))
async def duration_callback(
    callback_query: CallbackQuery,
    callback_data: dict,
    session: AsyncSession,
) -> None:
    """Ответ количество часов сна < 8 < заносим в БД."""
    user = await user_crud.get_by_attribute(
        'telegram_id',
        callback_query.from_user.id,
        session,
    )
    utc_offset_hours = await get_utc_offset(user.location) / SECONDS_IN_HOUR
    current_datetime = datetime.now(
        timezone(timedelta(hours=utc_offset_hours)),
    )
    yesterday_date = await get_yesterday(utc_offset_hours)
    sleep = await sleep_crud.get_last_sleep_obj(session, user)
    sleep_status = await get_sleep_status(
        sleep,
        utc_offset_hours,
        SleepMode.DURATION,
    )
    match sleep_status:
        case SleepMode.SLEEP_EXIST:
            media, reply_markup = (
                await get_banner(
                    menu_name=SleepMode.SLEEP_EXIST,
                    utc_offset_hours=int(utc_offset_hours),
                ),
                await get_sleep_exist_btns(level=2),
            )
        case SleepMode.VALID:
            media, reply_markup = await sleep_mode_menu(
                level=1,
                menu_name=SLEEP,
            )
            go_to_bed_time = await get_default_time(yesterday_date, 22)
            yes_no = callback_data.yes_no
            match yes_no:
                case 'yes':
                    wake_up_time = await get_default_time(current_datetime, 7)
                    sleep_duration = 9.0
                case 'no':
                    sleep_duration = 7.0
                    wake_up_time = await get_default_time(current_datetime, 5)

            if not sleep or (
                sleep.wake_up_time
                and (sleep.wake_up_time.date() != wake_up_time.date())
            ):
                sleep = await sleep_crud.create(
                    Sleep(
                        user_id=user.id,
                        go_to_bed_time=go_to_bed_time,
                        wake_up_time=wake_up_time,
                        sleep_duration=sleep_duration,
                    ),
                    session,
                )
            else:
                sleep.wake_up_time = wake_up_time
                sleep.go_to_bed_time = go_to_bed_time
                sleep.sleep_duration = sleep_duration
                await session.commit()
    await callback_query.message.answer_photo(
        photo=media.media,
        caption=media.caption,
        reply_markup=reply_markup,
    )
