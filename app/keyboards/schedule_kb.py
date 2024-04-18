from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.core.constants import (
    WORKOUTS, DIET, SLEEP, KB_TEXT_FOR_DIET,
    KB_TEXT_FOR_SLEEPING, KB_TEXT_FOR_TRAINING
)


calorie_control = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=KB_TEXT_FOR_DIET, callback_data=DIET
            )
        ],
    ],
)
ready_for_training = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=KB_TEXT_FOR_TRAINING, callback_data=WORKOUTS
            )
        ],
    ],
)
sleep_control = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=KB_TEXT_FOR_SLEEPING, callback_data=SLEEP
            )
        ],
    ],
)
