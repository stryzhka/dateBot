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
from aiogram import types, Dispatcher
import bot.db as db
from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.storage.base import StorageKey

router = Router()

@router.message(
    F.text.lower() == "смотреть анкеты",
    ProfileStates.static
)
async def start_watch(message: Message, state: FSMContext, bot: Bot):
    if db.is_watch_toggle(message.from_user.id) == 'False':
        await message.answer(
            text = 'твоя анкета отключена, твои лайки не учитываются :('
        )
    l = db.get_users_list()
    l.remove(db.get_user(message.from_user.id).user_id)
    for e in l:
        if db.get_user(e).watch_toggle == "False":
            print(db.get_user(e).username)
            l.remove(db.get_user(e).user_id)
    await state.update_data(
        users_len=len(l),
        pos=random.randint(0, len(l)-1),
        current=0
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
    await state.update_data(
        current=user.user_id
    )
    await state.set_state(ProfileStates.watching)

@router.message(
    F.text.lower() == '+',
    ProfileStates.watching 
)
async def match(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    if db.is_watch_toggle(message.from_user.id) == "True":
        await message.answer(
            text="симпатия отправлена"
        )
        try:
            db.add_match(message.from_user.id, data['current'])
            await bot.send_message(
                chat_id=data['current'],
                text = f"у тебя {len(db.get_got_id(data['current']))} симпатий"
                )
        except TelegramBadRequest:
            print("cant send request")    
            pass
    l = db.get_users_list()
    l.remove(db.get_user(message.from_user.id).user_id)
    for e in l:
        if db.get_user(e).watch_toggle == "False":
            print(db.get_user(e).username)
            l.remove(db.get_user(e).user_id)
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
    await state.update_data(
        current=user.user_id
    )
    img = FSInputFile(user.photo)
    await message.answer_photo(
            img,
            caption = f"{user.name}, {user.sex}\n{user.description}",
            reply_markup=make_keyboard(watching_kb)
        )
    
    print(data['current'])

@router.message(
    F.text.lower() == '-',
    ProfileStates.watching 
)
async def skip(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    l = db.get_users_list()
    l.remove(db.get_user(message.from_user.id).user_id)
    for e in l:
        if db.get_user(e).watch_toggle == "False":
            print(db.get_user(e).username)
            l.remove(db.get_user(e).user_id)
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
    await state.update_data(
        current=user.user_id
    )
    img = FSInputFile(user.photo)
    await message.answer_photo(
            img,
            caption = f"{user.name}, {user.sex}\n{user.description}",
            reply_markup=make_keyboard(watching_kb)
        )
    
    print(data['current'])

@router.message(
    F.text.lower() == "жалоба",
    ProfileStates.watching
)
async def send_complain(message: Message, bot: Bot, state: FSMContext):
    await message.answer(
        text="жалоба отправлена админам"
    )
    data = await state.get_data()      
    l = db.get_users_list()
    user = db.get_user(l[data['pos']])
    db.add_complain(user.user_id)
    await skip(message, state, bot)