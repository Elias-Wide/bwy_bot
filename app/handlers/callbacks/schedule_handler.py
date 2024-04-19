from aiogram import types, Router, F

from app.crud.schedule import schedule_crud
from app.core.constants import (
    WORKOUTS, DIET, SLEEP, TEXT_FOR_DIET,
    TEXT_FOR_SLEEPING, TEXT_FOR_TRAINING
)
from app.handlers.menu_processor import get_menu_content, calorie_counter
from app.keyboards.schedule_kb import (
    ready_for_training, sleep_control, calorie_control
)
from app import main

router = Router(name=__name__)


@router.callback_query(F.data == WORKOUTS)
async def training_callback(callback_query: types.CallbackQuery) -> None:

    media, reply_markup = await get_menu_content(level=1, menu_name=WORKOUTS)

    await callback_query.message.answer_photo(
        photo=media.media,
        caption=media.caption,
        reply_markup=reply_markup,
    )


@router.callback_query(F.data == SLEEP)
async def sleep_callback(callback_query: types.CallbackQuery) -> None:
    pass
    # media, reply_markup = await sleep_mode_menu(level=1, menu_name=SLEEP)

    # await callback_query.message.answer_photo(
    #     photo=media.media,
    #     caption=media.caption,
    #     reply_markup=reply_markup,
    # )


@router.callback_query(F.data == DIET)
async def calories_callback(callback_query: types.CallbackQuery) -> None:

    media, reply_markup = await calorie_counter(level=0, menu_name=DIET)

    await callback_query.message.answer_photo(
        photo=media.media,
        caption=media.caption,
        reply_markup=reply_markup,
    )


async def time_to_sleep() -> None:
    """Функция для уведомления пользователя о режиме сна."""
    users_tg_id = await schedule_crud.get_telegram_id(stop_reminder=SLEEP)

    for tg_id in users_tg_id:

        await main.bot.send_message(
            chat_id=tg_id,
            text=TEXT_FOR_SLEEPING,
            reply_markup=sleep_control
        )


async def time_to_training() -> None:
    """Функция для уведомления пользователя о тренировке."""
    users_tg_id = await schedule_crud.get_telegram_id(stop_reminder=WORKOUTS)

    for tg_id in users_tg_id:

        await main.bot.send_message(
            chat_id=tg_id,
            text=TEXT_FOR_TRAINING,
            reply_markup=ready_for_training
        )


async def time_to_calorie() -> None:
    """Функция для уведомления пользователя о норме калорий."""
    users_tg_id = await schedule_crud.get_telegram_id(stop_reminder=DIET)

    for tg_id in users_tg_id:

        await main.bot.send_message(
            chat_id=tg_id,
            text=TEXT_FOR_DIET,
            reply_markup=calorie_control
        )
