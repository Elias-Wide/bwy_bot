"""Модуль напоминаний."""

from aiogram import F, Router, types
from aiogram.exceptions import AiogramError
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app import main
from app.core.constants import (
    ADV,
    DIET,
    SLEEP,
    TEXT_FOR_DIET_SIMPLE,
    TEXT_FOR_SLEEPING,
    TEXT_FOR_TRAINING,
    TIME_CALORIES_FOR_SCHEDULER,
    TIME_SLEEP_FOR_SCHEDULER,
    TIME_TRAINING_FOR_SCHEDULER,
    TRAIN,
    WORKOUTS,
)
from app.core.logging import get_logger
from app.crud import schedule_crud, user_crud
from app.handlers.menu_processor import get_menu_content, sleep_mode_menu
from app.keyboards.schedule_kb import get_remind_button
from app.utils.schedule import (
    get_active_adv_hour,
    get_timedeltas_from_constant_time,
)

logger = get_logger(__name__)

router = Router(name=__name__)


@router.callback_query(F.data.in_({WORKOUTS, TRAIN}))
async def training_callback(
    callback_query: types.CallbackQuery,
    session: AsyncSession,
) -> None:
    """Отправляет картинку и меню при нажатии к тренировкам."""
    media, reply_markup = await get_menu_content(
        level=1,
        menu_name=WORKOUTS,
        user=await user_crud.get_by_attribute(
            'telegram_id',
            str(callback_query.from_user.id),
            session,
        ),
        session=session,
    )
    if type(callback_query.message) is Message:
        await callback_query.message.answer_photo(
            photo=media.media,
            caption=media.caption,
            reply_markup=reply_markup,
        )


@router.callback_query(F.data == SLEEP)
async def sleep_callback(
    callback_query: types.CallbackQuery,
    session: AsyncSession,
) -> None:
    """Отправляет картинку и меню при нажатии контроль сна."""
    media, reply_markup = await sleep_mode_menu(
        level=1,
        menu_name=SLEEP,
        user=await user_crud.get_by_attribute(
            'telegram_id',
            callback_query.from_user.id,
            session,
        ),
    )

    if type(callback_query.message) is Message:
        await callback_query.message.answer_photo(
            photo=media.media,
            caption=media.caption,
            reply_markup=reply_markup,
        )


@router.callback_query(F.data == DIET)
async def calories_callback(
    callback_query: types.CallbackQuery,
    session: AsyncSession,
) -> None:
    """Отправляет картинку и меню при нажатии контроль калорий."""
    media, reply_markup = await get_menu_content(
        level=0,
        menu_name=DIET,
        user=await user_crud.get_by_attribute(
            'telegram_id',
            str(callback_query.from_user.id),
            session,
        ),
        session=session,
    )
    if type(callback_query.message) is Message:
        await callback_query.message.answer_photo(
            photo=media.media,
            caption=media.caption,
            reply_markup=reply_markup,
        )


async def time_to_sleep_hourly() -> None:
    """Функция для уведомления пользователя о режиме сна."""
    timedeltas = await get_timedeltas_from_constant_time(
        TIME_SLEEP_FOR_SCHEDULER,
    )
    users_tg_id = await schedule_crud.get_telegram_id(
        stop_reminder=SLEEP,
        timedelta=timedeltas,
    )
    for tg_id in users_tg_id:
        try:
            await main.bot.send_message(
                chat_id=tg_id,
                text=TEXT_FOR_SLEEPING,
                reply_markup=get_remind_button(SLEEP),
            )
        except Exception:
            logger.info('пользователь заблокировал бота')


async def time_to_training_hourly() -> None:
    """Функция для уведомления пользователя о тренировке."""
    timedeltas = await get_timedeltas_from_constant_time(
        TIME_TRAINING_FOR_SCHEDULER,
    )
    users_tg_id = await schedule_crud.get_telegram_id(
        stop_reminder=WORKOUTS,
        timedelta=timedeltas,
    )

    for tg_id in users_tg_id:
        try:
            await main.bot.send_message(
                chat_id=tg_id,
                text=TEXT_FOR_TRAINING,
                reply_markup=get_remind_button(WORKOUTS),
            )
        except Exception:
            logger.info('пользователь заблокировал бота')


async def time_to_calorie_hourly() -> None:
    """Функция для уведомления пользователя о норме калорий."""
    timedeltas = await get_timedeltas_from_constant_time(
        TIME_CALORIES_FOR_SCHEDULER,
    )
    users_tg_id = await schedule_crud.get_telegram_id(
        stop_reminder=DIET,
        timedelta=timedeltas,
    )
    for tg_id in users_tg_id:
        try:
            await main.bot.send_message(
                chat_id=tg_id,
                text=TEXT_FOR_DIET_SIMPLE,
                reply_markup=get_remind_button(DIET),

            )
        except Exception:
            logger.info('пользователь заблокировал бота')


async def time_to_adv_hourly() -> None:
    """Функция для для рекламных анонсов."""
    time_adv_for_schedule = await get_active_adv_hour()
    if time_adv_for_schedule:
        timedeltas = await get_timedeltas_from_constant_time(
            time_adv_for_schedule,
        )
        list_hours = tuple(
            int(hour) for hour in time_adv_for_schedule.split(',')
        )
        relation_hour_offset = dict(zip(timedeltas, list_hours))
        for item in timedeltas:
            advertisment = await schedule_crud.get_adv_by_hour(
                relation_hour_offset[item],
            )
            users_tg_id = []
            users_tg_id.clear()
            users_tg_id = await schedule_crud.get_telegram_id(
                stop_reminder=ADV,
                timedelta=item,
                gender=advertisment.gender,
            )
            for tg_id in users_tg_id:
                try:
                    if advertisment.image:
                        await main.bot.send_photo(
                            chat_id=tg_id,
                            photo=types.FSInputFile(advertisment.image),
                            caption=advertisment.text,
                            parse_mode='HTML',
                            reply_markup=None,
                        )
                    else:
                        await main.bot.send_message(
                            chat_id=tg_id,
                            text=advertisment.text,
                            parse_mode='HTML',
                            reply_markup=None,
                        )
                except AiogramError as aio_err:
                    logger.info(aio_err)
