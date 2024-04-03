from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from app.core.logging import get_logger
from app.lexicon.lexicon import LEXICON
from app.keyboards import create_mode_kb, create_select_training_kb
import sys


router = Router()

logger = get_logger('__name__')


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text=LEXICON['/start'],
        reply_markup=await create_mode_kb()
    )

@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(
        text=LEXICON['/help'],
        reply_markup=await create_mode_kb()
    )

@router.message(Command(commands='die'))
async def process_help_command(message: Message):
    await message.answer(
        text=LEXICON['/die'],
        reply_markup=await create_mode_kb()
    )
    # logger.info(
    #     '''Exit such method is temporary because of polling 
    #        mode in fastapi calling Ctrl-C frozen terminal'''
    # )
    await sys.exit()

@router.message(F.text == LEXICON['mode']['trainings'])
async def process_trainings_command(message: Message):
    await message.answer(
        text=message.text,
        reply_markup=await create_select_training_kb()
    )
