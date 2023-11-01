import asyncio
import sys
import logging
import db_module
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.fsm.state import StatesGroup, State
from aiogram import F

TOKEN = '6333638829:AAGwXlXo7HjVvq0Fn5D83VofbH4LJljpXyA'
dp = Dispatcher()

class Form(StatesGroup):
    sex = State()
    name = State()
    description = State()
    photo = State()
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    if db_module.exist(message.from_user.id):
        await message.answer(f'ваш аккаунт уже зарегистрирован')
    else:
        kb = [
            [types.KeyboardButton(text='создать анкету')]
        ]
        kb = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True
        )
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
        await message.answer(f'привет, {hbold(message.from_user.full_name)}\nдобавляю тебя в базу данных', reply_markup=keyboard)
        db_module.add_user(message.from_user.id, message.from_user.username)

@dp.message(F.text.lower() == 'создать анкету')
async def create_profile(message: types.Message):
    await message.reply('ну ща создадим')

async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())