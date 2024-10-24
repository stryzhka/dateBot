import random
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from aiogram.utils.markdown import hbold
from aiogram.fsm.context import FSMContext
from aiogram import F

from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile
from bot.keyboards import make_keyboard, available_sex, profile_kb, static_kb, profile_kb1,  start_kb, watching_kb
from bot.states import ProfileStates
from bot.misc import Bot
from aiogram import types
import bot.db as db
from aiogram import Router

router = Router()

@router.message(
    F.text.lower() == "смотреть анкеты",
    ProfileStates.static
)
async def start_watch(message: Message, state: FSMContext, bot: Bot):
    l = db.get_users_list()
    l.remove(db.get_user(message.from_user.id).user_id)
    await state.update_data(
        users_len=len(l),
        pos=random.randint(0, len(l)-1)
    )
    data = await state.get_data()
    user = db.get_user(l[data['pos']])
    print(user.name)
    img = FSInputFile(user.photo)
    await message.answer_photo(
        img,
        caption = f"{user.name}, {user.sex}\n{user.description}",
        reply_markup=make_keyboard(watching_kb)
    )
    await state.set_state(ProfileStates.watching)

@router.message(
    F.text.lower() == '+',
    ProfileStates.watching 
)
async def match(message: Message, state: FSMContext, bot: Bot):
    await message.answer(
        text="симпатия отправлена"
    )
    l = db.get_users_list()
    l.remove(db.get_user(message.from_user.id).user_id)
    data = await state.get_data()
    print(data['pos'], len(l))
    if data['pos'] + 1 >= len(l):
        await state.update_data(
            pos=0
        )
    else:
        await state.update_data(
            pos=data['pos'] + 1
        )
    data = await state.get_data()
        
    user = db.get_user(l[data['pos']])
    img = FSInputFile(user.photo)
    await message.answer_photo(
        img,
        caption = f"{user.name}, {user.sex}\n{user.description}",
        reply_markup=make_keyboard(watching_kb)
    )

