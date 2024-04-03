@dp.message_handler(commands=['die'])
async def die (message: types.Message):
dp.stop_polling()
sys.exit()