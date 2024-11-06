from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from aiogram.utils.markdown import hbold
from aiogram.fsm.context import FSMContext
from aiogram import F

from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile
from bot.keyboards import make_keyboard, available_sex, profile_kb, static_kb, profile_kb1,  start_kb, got_match_kb
from bot.states import ProfileStates
from bot.misc import Bot
from aiogram import types
import bot.db as db
from aiogram import Router
from bot.text.MatchesText import MatchesText

router = Router()

@router.message(
    F.text.lower() == 'симпатии',
    ProfileStates.static
)
async def start_watch_matches(message: Message, state: FSMContext, bot: Bot):
    l = db.get_matches(message.from_user.id)
    print(l)
    if (len(l) > 0):
        await state.update_data(
            match_index=0
        )
        data = await state.get_data()
        img = FSInputFile(l[data['match_index']].photo)
        await message.answer_photo(
            img,
            caption = f"{l[data['match_index']].name}, {l[data['match_index']].sex}\n{l[data['match_index']].description}",
            reply_markup=make_keyboard(got_match_kb)
        )
        await state.set_state(ProfileStates.watching_matches)
    else:
        await message.answer(
        text=MatchesText.NO_LIKES()
    )
        
@router.message(
    F.text.lower() == '<3',
    ProfileStates.watching_matches
)
async def match_like(message: Message, state: FSMContext, bot: Bot):
    l = db.get_matches(message.from_user.id)
    data = await state.get_data()
    #print(l[data['match_index']].username)
    await message.answer(
        text=MatchesText.SENT_MATCH(l[0].username)
    )
    await bot.send_message(
        chat_id=l[0].user_id,
        text=MatchesText.GOT_MATCH(db.get_user(message.from_user.id).username)
    )

    db.remove_match(l[0].user_id, message.from_user.id)
    l = db.get_matches(message.from_user.id)
    #print("index", data['match_index'])
    #print("len", len(l))
    if len(l) == 0:
        await message.answer(
            text=MatchesText.END_LIKES(),
            reply_markup=make_keyboard(static_kb)
        )
        await state.set_state(ProfileStates.static)
    else:
        await state.update_data(
            #match_index=data['match_index'] + 1
        )
        data = await state.get_data()
        img = FSInputFile(l[0].photo)
        await message.answer_photo(
            img,
            caption = f"{l[data['match_index']].name}, {l[data['match_index']].sex}\n{l[data['match_index']].description}",
            reply_markup=make_keyboard(got_match_kb)
        )

@router.message(
    F.text.lower() == 'фу',
    ProfileStates.watching_matches
)
async def match_like(message: Message, state: FSMContext, bot: Bot):
    l = db.get_matches(message.from_user.id)
    #print(l)
    data = await state.get_data()
    #print(f'L len: {len(l)}, match_index: {data['match_index']}')
    #print(l[data['match_index']].username)
    db.remove_match(l[0].user_id, message.from_user.id)
    l = db.get_matches(message.from_user.id)
    #print("index", data['match_index'])
    #print("len", len(l))
    if len(l) == 0:
        await message.answer(
            text=MatchesText.END_LIKES(),
            reply_markup=make_keyboard(static_kb)
        )
        await state.set_state(ProfileStates.static)
    else:
        #await state.update_data(
        #    match_index=data['match_index'] + 1
        #)
        #data = await state.get_data()
        img = FSInputFile(l[0].photo)
        await message.answer_photo(
            img,
            caption = f"{l[data['match_index']].name}, {l[data['match_index']].sex}\n{l[data['match_index']].description}",
            reply_markup=make_keyboard(got_match_kb)
        )
    