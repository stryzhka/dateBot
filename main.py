import asyncio
import sys
import logging
import db_module
import io
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile
from service_module import make_keyboard, available_sex, profile_kb

TOKEN = '6333638829:AAGwXlXo7HjVvq0Fn5D83VofbH4LJljpXyA'
dp = Dispatcher()

class Profile(StatesGroup):
    choosing_sex = State()
    choosing_name = State()
    choosing_description = State()
    choosing_photo = State()
    static = State()
    profile_ended = State()
@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    if db_module.exist(message.from_user.id):
        kb = [
            [types.KeyboardButton(text='создать анкету')]
        ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True
        )
        await message.answer(f'нажми на кнопку создать анкету', reply_markup=keyboard)
        await state.set_state(Profile.static)
    else:
        kb = [
            [types.KeyboardButton(text='создать анкету')]
        ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True
        )

        await message.answer(f'привет, {hbold(message.from_user.full_name)}\n, создай анкету', reply_markup=keyboard)
        db_module.add_user(message.from_user.id, message.from_user.username)
        await state.set_state(Profile.static)

@dp.message(
    F.text.lower() == 'создать анкету',
    Profile.static
)
@dp.message(F.text.lower() == 'изменить анкету', Profile.profile_ended)
async def create_profile_begin(message: types.Message, state: FSMContext):
    await message.reply('введи свое имя (ну или что-нибудь смешное хз)', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Profile.choosing_name)

@dp.message(
    Profile.choosing_name
)
async def create_profile_sex(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(
        text='теперь выбери свой гендер или пол или как там это называется',
        reply_markup=make_keyboard(available_sex)
    )
    await state.set_state(Profile.choosing_sex)
@dp.message(
    Profile.choosing_sex,
    F.text.in_(available_sex)
)
async def create_profile_description(message: Message, state: FSMContext):
    await state.update_data(
        sex=message.text
    )
    await message.answer(
        text='напиши описание - чем любишь заниматься, любимые группы, увлечения, все такое',
        reply_markup = types.ReplyKeyboardRemove()
    )
    await state.set_state(Profile.choosing_description)

@dp.message(
    Profile.choosing_description,
    F.text.len() > 128
)
async def create_profile_description_fail(message: Message, state: FSMContext):
    await message.answer(
        text='описание слишком длинное! попробуй сократить, максимум - 128 символов',
    )
    await state.set_state(Profile.choosing_description)

@dp.message(
    Profile.choosing_description,
    F.text.len() <= 128
)
async def create_profile_photo(message: Message, state: FSMContext):
    await state.update_data(
        description=message.text
    )
    await message.answer(
        text='скинь фотку для анкеты',
    )
    await state.set_state(Profile.choosing_photo)

@dp.message(
    Profile.choosing_photo,
    F.photo
)
async def profile_finished(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(photo_id=message.photo[-1].file_id)
    data = await state.get_data()
    _desc = f"{data['name']},{data['sex']}\n{data['description']}"
    await message.answer_photo(
        message.photo[-1].file_id,
        caption=_desc
    )
    await message.answer(
        text='анкета готова!',
        reply_markup=make_keyboard(profile_kb)
    )
    await state.set_state(Profile.profile_ended)

@dp.message(
    Profile.profile_ended,
    F.text == 'сохранить анкету'
)
async def profile_save(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    await message.answer(
        text=str(data)
    )

async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())