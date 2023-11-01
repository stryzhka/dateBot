import asyncio
import sys
import logging
import db_module
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

TOKEN = '6333638829:AAGwXlXo7HjVvq0Fn5D83VofbH4LJljpXyA'
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    if db_module.exist(message.from_user.id):
        await message.answer(f'stupid bitch')
    else:
        await message.answer(f'hello {hbold(message.from_user.full_name)}\nadding you to db')
        db_module.add_user(message.from_user.id, message.from_user.username)

@dp.message()
async def echo_handler(message: types.Message) -> None:
    try:
        await message.answer(f'go fuck yourself, {db_module.getUser(message.from_user.id).user_id}')
    except TypeError:
        await message.answer('da fuck')

async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

#jopius
