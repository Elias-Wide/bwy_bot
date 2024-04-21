from aiogram.types import InlineKeyboardMarkup, InputMediaPhoto

from app.keyboards.sleep_kb import (
    get_sleep_back_btns,
    get_sleep_back_btns_duration,
    get_sleep_select_btns,
)
from app.utils.utils import get_banner


async def sleep_mode_menu(
    level: int,
    menu_name: str,
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    return (
        await get_banner(menu_name),
        get_sleep_select_btns(level=level),
    )


async def go_to_bed_menu(
    level: int,
    menu_name: str,
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    """Ответ времени отхода ко сну."""
    return (
        await get_banner(menu_name),
        get_sleep_back_btns(level=level),
    )


async def wake_up_menu(
    level: int,
    menu_name: str,
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    """Ответ времени пробуждения."""
    return (
        await get_banner(menu_name),
        get_sleep_back_btns(level=level),
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
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    """Ввод продолжительности сна."""
    return (
        await get_banner(menu_name),
        get_sleep_back_btns(level=level),
    )
