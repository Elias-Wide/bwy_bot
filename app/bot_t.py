import asyncio 
from aiogram import Bot, types 
from aiogram import Dispatcher 


API_TOKEN = '6134898896:AAFX1qIspn8tPqhHGwUHj5yGYn7tQUmSf7M'
bot = Bot(token=API_TOKEN) 
dp = Dispatcher()


is_running = False
async def start_cycle(message: types.Message): 
    global is_running 
    is_running = True 

    while is_running: 
        await message.answer("Цикл выполняется...") 
        await asyncio.sleep(1) 


async def stop_cycle(message: types.Message): 
    global is_running 
    is_running = False 
    await message.answer("Цикл остановлен.") 


@dp.message(Commands=['start']) 
async def start_command(message: types.Message): 
    await start_cycle(message) 


@dp.message(Commands=['stop']) 
async def stop_command(message: types.Message): 
    await stop_cycle(message) 


if __name__ == '__main__': 
    dp.start_polling(dp, skip_updates=True)
