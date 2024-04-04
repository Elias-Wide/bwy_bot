import sys

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from app.core.config import settings
from app.core.logging import get_logger
from app.keyboards import create_mode_kb, create_select_training_kb
from app.lexicon.lexicon import LEXICON

router = Router()

logger = get_logger(__name__)


@router.message(CommandStart())
async def process_start_command(message: Message) -> None:
    await message.answer(
        text=LEXICON['/start'],
        reply_markup=await create_mode_kb(),
    )


@router.message(Command(commands='die'))
async def process_die_command(message: Message) -> None:
    await message.answer(
        text=LEXICON['/die'],
        reply_markup=await create_mode_kb(),
    )
    if not settings.webhook_mode:
        logger.info('Можно выключать WEBHOOK_MODE:')
        logger.info(settings.webhook_mode)
        await sys.exit()
    else:
        logger.info('Можно выключать WEBHOOK_MODE:')
        logger.info(settings.webhook_mode)


@router.message(Command(commands='help'))
async def process_help_command(message: Message) -> None:
    await message.answer(
        text=LEXICON['/help'],
        reply_markup=await create_mode_kb(),
    )


@router.message(F.text == LEXICON['mode']['trainings'])
async def process_trainings_command(message: Message) -> None:
    await message.answer(
        text=message.text,
        reply_markup=await create_select_training_kb(),
    )
